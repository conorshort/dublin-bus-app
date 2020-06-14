from rest_framework import serializers
from .models import BusStop

class BusStopSerializer(serializers.ModelSerializer):
    class Meta: 
        model = BusStop
        fields = ( 'stopid', 
        'displaystopid',
        'shortname', 
        'shortnamelocalized',
        'fullname',
        'latitude',
        'longitude',
        'lastupdated',
        'operator',
        'op_type',
        'routes')



       