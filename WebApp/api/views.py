from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import BusStop
from .serializers import BusStopSerializer
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.http import HttpResponse

class BusStopViewSet(viewsets.ModelViewSet):
    queryset = BusStop.objects.all()
    serializer_class = BusStopSerializer

    def get_queryset(self):

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
            FROM dublin_bus_test.all_bus_stops \
            as s HAVING distance < %s \
            ORDER BY distance;" % (latitude, longitude, latitude, radius) 


        queryset = BusStop.objects.raw(sql)
        serializer = BusStopSerializer(queryset, many=True)

        return serializer.data

    