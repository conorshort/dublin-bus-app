from rest_framework import serializers
from .models import BusStop

class BusStopSerializer(serializers.ModelSerializer):
    class Meta: 
        model = BusStop
        fields = ( 'stopid', 
        'shortnamelocalized',
        'fullname',
        'latitude',
        'longitude',
        'lastupdated',
        'routes')



       