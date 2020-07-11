from django.db import models
from django.templatetags.static import static
from .gtfsabstract import GTFSManager, AbstractGTFS
from .gtfsroute import GTFSRoute
from .gtfscalendar import GTFSCalendar
import datetime
from django.db.models import F
# =================== TRIPS ===================


class GTFSTripManager(GTFSManager):

    def get_stops_between(self, origin_id, destination_id, route_name, head_sign):
        """ Given two stop IDs, a route and a headsign, get a list of intermediate stops """

        today = datetime.datetime.today()

        shape_id_queryset = GTFSTrip.objects.filter(
            route__route_name=route_name,
            calendar__start_date__lte=today,
            calendar__end_date__gte=today).values("shape_id", towards=F("gtfsstoptime__stop_headsign")).distinct()

        print(shape_id_queryset)
        shape_id = shape_id_queryset.filter(towards=head_sign).values("shape_id")
        print(shape_id)
        stops = self.stops_on_route(shape_id)

        origin_seq = stops.filter(stop__plate_code=origin_id).values("stop_sequence")
        dest_seq = stops.filter(stop__plate_code=destination_id).values("stop_sequence")

        these_stops = stops.filter(stop_sequence__gte=origin_seq,
                                   stop_sequence__lte=dest_seq)


        print(these_stops)

    def stop_on_route(self, shape_id):
        ''' Given a routeshape get all stops on the route'''

        trip = GTFSTrip.objects.filter(shape_id=shape_id).first()
        return trip.gtfsstoptime_set

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
