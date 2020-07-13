from django.db import models
from django.templatetags.static import static
from .gtfsabstract import GTFSManager, AbstractGTFS
from .gtfsroute import GTFSRoute
from .gtfscalendar import GTFSCalendar
import datetime
from django.db.models import F
# =================== TRIPS ===================


class GTFSTripManager(GTFSManager):
    # TODO: See if timetables can be used to further narrow down if necessary
    def get_stops_between(self, origin_id, destination_id, route_name, headsign=False, get_objects=False):
        """ Given two stop IDs and a route, get a list of lists of intermediate stops 
        
        It is possible (though hopefully rare) that there will be two possible sequences of stops
        between two stops id, so a list of lists is returned
        
        origin_id, destination_id: (Integers) should be plate codes for the stops, such as 7185
        route_name: (string), common name of the route, such as "39A"
        headsign (optional): (string), the headsign of the bus for this trip, such as "Ballymore"
        get_objects (options): (Boolean), return a list of stop objects in casefuther processing is needed
        """

        today = datetime.datetime.today()
        if headsign:
            shape_id_queryset = GTFSTrip.objects.filter(
                route__route_name=route_name,
                calendar__start_date__lte=today,
                calendar__end_date__gte=today,
                gtfsstoptime__stop_headsign=headsign).values("shape_id").distinct()
        else:
            shape_id_queryset = GTFSTrip.objects.filter(
                route__route_name=route_name,
                calendar__start_date__lte=today,
                calendar__end_date__gte=today).values("shape_id").distinct()

        stop_query_set = []
        stops_as_lists = []
        for shape in shape_id_queryset:
            shape = shape["shape_id"]
            stops = self.stops_on_route(shape)

            origin_seq = stops.filter(
                stop__plate_code=origin_id).values("stop_sequence")
            dest_seq = stops.filter(
                stop__plate_code=destination_id).values("stop_sequence")
            these_stops = stops.filter(stop_sequence__gte=origin_seq,
                                       stop_sequence__lte=dest_seq)
            these_stops_list = list(these_stops.values("stop_sequence", plate_code=F("stop__plate_code")))
            if these_stops and these_stops_list not in stops_as_lists:
                stop_query_set.append(these_stops)
                stops_as_lists.append(these_stops_list)
        if get_objects:
            return stop_query_set
        else:
            return stops_as_lists


    def stops_on_route(self, shape_id):
        ''' Given a routeshape get all stops on the route'''

        trip = GTFSTrip.objects.filter(shape_id=shape_id).first()
        return trip.gtfsstoptime_set.all()

class GTFSTrip(AbstractGTFS):
    route = models.ForeignKey(GTFSRoute, on_delete=models.CASCADE)
    calendar = models.ForeignKey(GTFSCalendar, on_delete=models.CASCADE)
    trip_id = models.CharField(primary_key=True, max_length=70)
    shape_id = models.CharField(max_length=70)
    trip_headsign = models.CharField(max_length=200)
    direction_id = models.IntegerField()

    _text_file = "trips.txt"

    objects = GTFSTripManager()

    def _dict_proc_func(self, trip_dict, agency_dict):

        agency_id = agency_dict["id"]
        trip_dict["calendar"] = GTFSCalendar(agency_service_id=f'{agency_id}_{trip_dict["service_id"]}')

        trip_dict["route"] = GTFSRoute(route_id=trip_dict["route_id"])

        return trip_dict
        
    class Meta:
        managed = True
        db_table = 'gtfs_trips'
