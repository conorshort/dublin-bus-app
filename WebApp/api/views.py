from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import BusStop, GTFSRoute, GTFSShape, GTFSStopTime, GTFSTrip
from .serializers import BusStopSerializer, GTFSRouteSerializer, GTFSShapeSerializer, GTFSStopTimeSerializer, GTFSTripSerializer

class BusStopViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BusStop.objects.all()
    serializer_class = BusStopSerializer

    # giving params longitude, latitudeand radius, API will return all the stops with in radius
    # usage example: /api/stops/nearby?longitude=-6.263695&latitude=53.3522411111&radius=0.1
    @action(detail=False)
    def nearby(self, request):

        longitude = self.request.query_params.get('longitude')
        latitude= self.request.query_params.get('latitude')
        radius = self.request.query_params.get('radius')
        
        # SQL statement that will find the stops that are within given radius
        sql = "SELECT *, ( 3959 * acos ( cos ( radians( %s ) )\
            * cos( radians( s.latitude ) )\
            * cos( radians( s.longitude ) \
                - radians( %s ) )\
            + sin ( radians( %s ) )\
            * sin( radians( s.latitude ) ))) \
            AS distance \
            FROM bus_data.bus_stops \
            as s HAVING distance < %s \
            ORDER BY distance;" % (latitude, longitude, latitude, radius) 

        queryset = BusStop.objects.raw(sql)
        serializer = BusStopSerializer(queryset, many=True)

        return Response(serializer.data)

class GTFSRouteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GTFSRoute.objects.all()
    serializer_class = GTFSRouteSerializer

class GTFSShapeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GTFSShape.objects.all()
    serializer_class = GTFSShapeSerializer

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
            unique_tripid = tripid + ':'+ stopSequence
            queryset = queryset.filter(unique_trip_id=unique_tripid)

        # if only tripid paramater is given, 
        # filter stoptime data by trip_id
        elif tripid :
            queryset = queryset.filter(trip_id=tripid)

        serializer = GTFSStopTimeSerializer(queryset, many=True)

        return Response(serializer.data)

    

class GTFSTripViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GTFSTrip.objects.all()
    serializer_class = GTFSTripSerializer

    @action(detail=False)
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

    