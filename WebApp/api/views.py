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

from prediction import predict_journey_time, get_models_name


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
    # if yes, get journey plan for google direction API,
    # and predict the journey time for dublin bus transit
    # if missing any parameter from request
    # return a http 400 response with message
    if not(origin and destination and departureUnix):

        response_data = {'message': 'Missing Parameter'}
        return JsonResponse(response_data, status=400)
        
    
    url = 'https://maps.googleapis.com/maps/api/directions/json'

    # defining a params dict for the parameters to be sent to the API 
    PARAMS = {'origin' : origin,
            'destination' : destination,
            'key' : GOOGLE_DIRECTION_KEY,
            'transit_mode' : 'bus',
            'mode' : 'transit'} 
            
    # sending get request and saving the response as response object 
    r = requests.get(url = url, params = PARAMS) 
    
    # extracting data in json format 
    data = r.json() 
    if data['status'] != 'OK':
        return JsonResponse(data)



    # check if the specific route model exist
    # if yes: predict the jourent time
    # if not: response google direction API data 

    lines = [modelName.replace('.pkl', '') for modelName in get_models_name()]

    try:
        # copy another data for editing
        newData = copy.deepcopy(data) 
        steps = newData['routes'][0]['legs'][0]['steps']

        totalDuration = 0

        # forloop steps from google direction API response
        for i in range(len(steps)):


            # check if the step travel_mode is TRANSIT
            if steps[i]['travel_mode'] != 'TRANSIT':
                duration = int(steps[i]['duration']['text'].split()[0])
                totalDuration += duration
                continue
            
            # check if the line model exist 
            lineId = steps[i]['transit_details']['line']['short_name'].upper()
            if ('route_'+lineId) not in lines:
                continue
            arrStopCoordination = steps[i]['transit_details']['arrival_stop']['location']
            depStopCoordination = steps[i]['transit_details']['departure_stop']['location']

            # get stop id by stop coordinate
            arrStopId = SmartDublinBusStop.objects.get_nearest_id \
                (arrStopCoordination['lat'], arrStopCoordination['lng'])
            
            depStopId = SmartDublinBusStop.objects.get_nearest_id \
                (depStopCoordination['lat'], depStopCoordination['lng'])

            # get stops between origin and destination stops
            headsign = steps[i]['transit_details']['headsign']
            origin_time = steps[i]['transit_details']['departure_time']['text']
            
            stops = GTFSTrip.objects.get_stops_between(depStopId, arrStopId, lineId, origin_time=origin_time, headsign=headsign)[0]

            # print('depStopId', depStopId)
            # print('arrStopId', arrStopId)
            # print('lineId', lineId)
            print('stops', stops)



            # store stops info in data json for response 
            newData['routes'][0]['legs'][0]['steps'][i]['transit_details']['stops'] = stops


            # get all the segmentid by stopsid
            segments = []
            for index in range(len(stops)-1):
                segments.append(stops[index]['plate_code'] + '-' + stops[index+1]['plate_code'])
            
            
            # predict traveling time for all segmentid
            lineId = steps[i]['transit_details']['line']['short_name']
            journeyTime = predict_journey_time(lineId, segments, int(departureUnix))

            totalDuration += int(journeyTime) // 60

            # update duration value in newData to our journey prediction
            newData['routes'][0]['legs'][0]['steps'][i]['duration']['text'] = str(int(journeyTime) // 60) + ' mins'

        newData['routes'][0]['legs'][0]['duration']['text'] = str(totalDuration) + ' mins'
        print("=====google prediction journey time:", data['routes'][0]['legs'][0]['duration']['text'], "========")

        return JsonResponse(newData, safe=False)

    except Exception as e:
        print("type error:", str(e))
        return JsonResponse(data, safe=False)
   
        
        
    
    
    


    
