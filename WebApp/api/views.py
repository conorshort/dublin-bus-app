from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import BusStop
from .serializers import BusStopSerializer

class BusStopViewSet(viewsets.ModelViewSet):
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
            FROM bus_data.sd_bus_stops \
            as s HAVING distance < %s \
            ORDER BY distance;" % (latitude, longitude, latitude, radius) 

        queryset = BusStop.objects.raw(sql)
        
        # all_commenter_ids = list(queryset)
        # print(all_commenter_ids[0])
        serializer = BusStopSerializer(queryset, many=True)

        return Response(serializer.data)

    