from rest_framework import serializers
from api.models import SmartDublinBusStop, GTFSRoute, GTFSShape, GTFSStopTime, GTFSTrip


class SmartDublinBusStopSerializer(serializers.ModelSerializer):
    class Meta: 
        model = SmartDublinBusStop
        fields = ( 'stopid', 
        'shortnamelocalized',
        'fullname',
        'latitude',
        'longitude',
        'lastupdated',
        'routes',
        'localname')


class GTFSRouteSerializer(serializers.ModelSerializer):
    class Meta: 
        model = GTFSRoute
        fields = ( 'route_id', 'route_name')


class GTFSShapeSerializer(serializers.ModelSerializer):
    class Meta: 
        model = GTFSShape
        fields = ( 'unique_point_id', 
        'shape_id',
        'shape_pt_lat',
        'shape_pt_lon',
        'shape_pt_sequence')


class GTFSStopTimeSerializer(serializers.ModelSerializer):
    class Meta: 
        model = GTFSStopTime
        fields = ( 'unique_trip_id', 
        'trip_id',
        'arrival_time',
        'departure_time',
        'stop_id',
        'stop_sequence',
        'stop_headsign')

class GTFSTripSerializer(serializers.ModelSerializer):
    class Meta: 
        model = GTFSTrip
        fields = ( 'route_id', 
        'trip_id',
        'shape_id',
        'trip_headsign',
        'direction_id')
