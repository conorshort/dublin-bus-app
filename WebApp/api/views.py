from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import action
from api.models import SmartDublinBusStop, GTFSRoute, GTFSShape, GTFSStopTime, GTFSTrip
from .serializers import SmartDublinBusStopSerializer, GTFSRouteSerializer, GTFSShapeSerializer, GTFSStopTimeSerializer, GTFSTripSerializer
from datetime import datetime
from django.db.models import F
import requests
from dublin_bus.config import GOOGLE_DIRECTION_KEY
import pandas as pd
import copy 
import json
from geopy.distance import great_circle
from .direction import directionUntilFirstTransit, secondsIntToTimeString, meterIntToKMString


class SmartDublinBusStopViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SmartDublinBusStop.objects.all()
    serializer_class = SmartDublinBusStopSerializer

    # giving params longitude, latitudeand radius, API will return all the stops with in radius
    # usage example: /api/stops/nearby?longitude=-6.263695&latitude=53.3522411111&radius=0.1
    @action(detail=False)
    def nearby(self, request):

        longitude = self.request.query_params.get('longitude')
        latitude = self.request.query_params.get('latitude')
        radius = self.request.query_params.get('radius')

        # Check if value of longitude and latitude are given
        if longitude and latitude:

            # if radius value is not given, set radius value as 0.3(km)
            if radius is None:
                radius = '0.3'

            # SQL statement that will find the stops that are within given radius
            sql = "SELECT *, ( 3959 * acos ( cos ( radians( %s ) )\
                * cos( radians( s.latitude ) )\
                * cos( radians( s.longitude ) \
                    - radians( %s ) )\
                + sin ( radians( %s ) )\
                * sin( radians( s.latitude ) ))) \
                AS distance \
                FROM bus_data.sd_bus_stops \
                as s HAVING distance < %s \
                ORDER BY distance;" % (latitude, longitude, latitude, radius)

            queryset = SmartDublinBusStop.objects.raw(sql)
            
            serializer = SmartDublinBusStopSerializer(queryset, many=True)

            return Response(serializer.data)

        # If missing longitude and latitude value, return error message
        else:
            content = {'message': 'Longitude and latitude fields are required'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class GTFSRouteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GTFSRoute.objects.all()
    serializer_class = GTFSRouteSerializer

    @action(detail=False)
    def routename(self, response):
        ''' Return a list of distinct route names found in the db '''
        route_queryset = GTFSTrip.objects.get_all_routes()
        return Response(route_queryset)

    @action(detail=False)
    def variations(self, request):
        ''' Given a routename and direction get all variations of a route'''
        route_name = request.GET.get('name')
        inbound = request.GET.get("inbound")

        today = datetime.today()

        # Get distint shape ids and destinations for the given route name and direction
        # that are currently in service
        shape_id_queryset = GTFSTrip.objects.filter(
            route__route_name=route_name,
            direction_id=inbound,
            calendar__start_date__lte=today,
            calendar__end_date__gte=today).values("shape_id", towards=F("gtfsstoptime__stop_headsign")).distinct()

        return Response(shape_id_queryset)

    @action(detail=False)
    def stops(self, request):
        ''' Given a routeshape get all stops on the route'''
        shape_id = request.GET.get('shape')

        stops = GTFSTrip.objects.stops_on_route(shape_id).values(
                    stop_name=F("stop__stop_name"),
                    seq=F("stop_sequence"),
                    id=F("stop_id"),
                    lat=F("stop__stop_lat"),
                    lon=F("stop__stop_lon"))

        return Response(stops)


class GTFSShapeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GTFSShape.objects.all()
    serializer_class = GTFSShapeSerializer

    @action(detail=False)
    def geo_json(self, request):
        routename = request.GET.get("routename")
        inbound = request.GET.get("inbound")

        today = datetime.today()

        shape_queryset = GTFSTrip.objects.filter(
            route__route_name=routename,
            direction_id=inbound,
            calendar__start_date__lte=today,
            calendar__end_date__gte=today,).values("shape_id", towards=F("gtfsstoptime__stop_headsign")).distinct()

        shape_geo_jsons = []

        for shape in shape_queryset:
            geojsonFeature = {
                "type": "Feature",
                "properties": {
                    "name": routename,
                    "shapeId": shape["shape_id"],
                    "popupContent": f"{routename} towards {shape['towards']}"
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates":  GTFSShape.objects.get_points_by_id(shape["shape_id"])
                }
            }

            shape_geo_jsons.append(geojsonFeature)

        return Response(shape_geo_jsons)


class GTFSStopTimeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GTFSStopTime.objects.all()
    serializer_class = GTFSStopTimeSerializer

    @action(detail=False)
    def stoptime(self, response):
        queryset = GTFSStopTime.objects.all()
        tripid = self.request.query_params.get('tripid')
        stopSequence = self.request.query_params.get('stopsequence')

        # if both tripid and stopSequence paramaters are given,
        # filter stoptime data by unique_trip_id
        if tripid and stopSequence:
            unique_tripid = tripid + ':' + stopSequence
            queryset = queryset.filter(unique_trip_id=unique_tripid)

        # if only tripid paramater is given,
        # filter stoptime data by trip_id
        elif tripid:
            queryset = queryset.filter(trip_id=tripid)

        serializer = GTFSStopTimeSerializer(queryset, many=True)

        return Response(serializer.data)

    @action(detail=False)
    def timetable(self, response):
        ''' Given a shape id and stop id, get a timetable for that route at that stop '''
        shape_id = self.request.query_params.get("shape")
        stop_id = self.request.query_params.get("stop_id")

        trips = GTFSTrip.objects.filter(shape_id=shape_id)

        calendars = trips.values("calendar__display_days").distinct()

        trips_by_calendar = {}
        for calendar in calendars:
            calendar_days = calendar["calendar__display_days"]
            t = trips.filter(calendar__display_days=calendar_days,
                             gtfsstoptime__stop_id=stop_id)

            trips_by_calendar[calendar_days] = t.values(
                time=F("gtfsstoptime__departure_time"))

        return Response(trips_by_calendar)


class GTFSTripViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GTFSTrip.objects.all()
    serializer_class = GTFSTripSerializer

    @ action(detail=False)
    def trips(self, response):
        queryset = GTFSTrip.objects.all()
        routeid = self.request.query_params.get('routeid')
        shapeid = self.request.query_params.get('shapeid')

        # if shapeid paramater is given, filter trips data by shapeid
        if shapeid:
            print(shapeid)
            queryset = queryset.filter(shape_id=shapeid)

        # elseif routeid paramater is given, filter trips data by routeid
        elif routeid:
            queryset = queryset.filter(route_id=routeid)
            print(routeid)

        serializer = GTFSTripSerializer(queryset, many=True)

        return Response(serializer.data)




def realtimeInfo(request, stop_id):
    r = requests.get(f"https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid={stop_id}&format=json%27")
    return JsonResponse(r.json() , safe=False)


def direction(request):

    # get given parameters 
    origin = request.GET.get('origin')
    destination = request.GET.get('destination')
    departureUnix = request.GET.get('departureUnix')

    # check if 3 papameter all given
    # if missing any parameter from request
    # return a http 400 response with message
    if not(origin and destination and departureUnix):

        response_data = {'message': 'Missing Parameter'}
        return JsonResponse(response_data, status=400)

    destination_coord = (destination.split(",")[0], destination.split(",")[1])
    
    newData = {'leg': {'steps' : []}}

    
    isFirstTimeRequest = True
    requestCount = 0

    while (requestCount <= 6) and ((isFirstTimeRequest) or  \
            ((great_circle((origin.split(",")[0], origin.split(",")[1]), destination_coord).meters) >= 50)):
         
        requestCount += 1

        data = directionUntilFirstTransit(origin, destination, departureUnix)

        if isFirstTimeRequest == True:
            newData['leg']['distance'] = {'value': 0, 'text': ''}
            newData['leg']['duration'] = {'value': 0, 'text': ''}
            newData['leg']['start_location'] = data['leg']['start_location']
            newData['leg']['start_address'] = data['leg']['start_address']
            newData['leg']['departure_time'] = data['leg']['departure_time']
   
        origin = str(data['leg']['end_location']['lat'])+","+ str(data['leg']['end_location']['lng'])
        departureUnix = data['leg']['departure_time']['value']


        if data['status'] != 'OK':
            return JsonResponse(data)

        # add reponsed steps' data to newData
        newData['leg']['distance']['value'] += int(data['leg']['distance']['value'])
        newData['leg']['duration']['value'] += int(data['leg']['duration']['value'])
        newData['leg']['distance']['text'] = meterIntToKMString(int(newData['leg']['distance']['value']))
        newData['leg']['duration']['text'] = secondsIntToTimeString(int(newData['leg']['duration']['value']))
        newData['leg']['end_location'] = data['leg']['end_location']
        newData['leg']['steps'] += data['leg']['steps']
        newData['leg']['arrival_time'] = data['leg']['arrival_time']

        isFirstTimeRequest = False


    return JsonResponse(newData, safe=False)

    # except Exception as e:
    #     print("type error:", str(e))
    #     return JsonResponse(data, safe=False)
   
        
        
    
    
    

 