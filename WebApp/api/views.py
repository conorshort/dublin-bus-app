from django.shortcuts import render
from rest_framework import viewsets
from .models import BusStop
from .serializers import BusStopSerializer

class BusStopViewSet(viewsets.ModelViewSet):
    queryset = BusStop.objects.all()
    serializer_class = BusStopSerializer

    # def get_queryset(self):
    #     longitude = self.request.query_params.get('longitude')
    #     latitude= self.request.query_params.get('latitude')
    #     radius = self.request.query_params.get('radius')

    #     location = Point(longitude, latitude)
    #     queryset = BusStop.objects.filter(location__distance_lte=(location, D(m=distance))).distance(location).order_by('distance')

    #     return queryset