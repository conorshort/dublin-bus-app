from django.db import models
from django.templatetags.static import static
from .gtfsabstract import GTFSManager, AbstractGTFS
from .gtfsroute import GTFSRoute
from .gtfscalendar import GTFSCalendar
from .gtfsstop import GTFSStop
import datetime
from django.db.models import F
# =================== TRIPS ===================


class GTFSTripManager(GTFSManager):

    # TODO: See if timetables can be used to further narrow down if necessary
    def get_stops_between(self, origin_plate_code, destination_plate_code, route_name, origin_time=None, headsign=None, get_objects=False):
        """ Given two stop IDs and a route, get a list of lists of intermediate stops
        It is possible (though hopefully rare) that there will be two possible sequences of stops
        between two stops id, so a list of lists is returned
        origin_id, destination_id: (Integers) should be plate codes for the stops, such as 7185
        route_name: (string), common name of the route, such as "39A"
        headsign (optional): (string), the headsign of the bus for this trip, such as "UCD"
        origin_time (optional): (int), the time in seconds that the bus should depart the origin stops
        get_objects (options): (Boolean), return a list of stop objects in case futher processing is needed
        """
        # Get today's date to fliter currently active routes
        today = datetime.datetime.today()

        # Round the origin time to the nearest minute
        if origin_time:
            am_or_pm = origin_time[-2:]
            origin_time = origin_time[:-2]
            hrs, mins = origin_time.split(":")
            origin_time = (int(hrs) * 3600) + (int(mins) * 60)
            if am_or_pm == "pm":
                origin_time += 43200
            print(origin_time)

        origin_id = GTFSStop.objects.get(plate_code=origin_plate_code).stop_id
        destination_id = GTFSStop.objects.get(
            plate_code=destination_plate_code).stop_id

        # Get shape_ids for the given route
        # If a headsign is provided add it to the filter
        print("getting stops")
        stop_query_set = []
        stops_as_lists = []

        if headsign and origin_time:
            # First try to get with all parameters given
            shape_id_queryset = None
            trips = GTFSTrip.objects.filter(
                route__route_name=route_name,
                calendar__start_date__lte=today,
                calendar__end_date__gte=today,
                gtfsstoptime__arrival_time__gte=(origin_time - 60),
                gtfsstoptime__departure_time__lte=(origin_time + 60),
                gtfsstoptime__stop_headsign=headsign,
                gtfsstoptime__stop_id=origin_id)


            if origin_time and not trips:
                print("none found, trying without headsign")
                # Then try without headsign, sometimes google's headsign doesn't match the gtfs data 
                shape_id_queryset = None
                trips = GTFSTrip.objects.filter(
                    route__route_name=route_name,
                    calendar__start_date__lte=today,
                    calendar__end_date__gte=today,
                    gtfsstoptime__arrival_time__gte=(origin_time - 60),
                    gtfsstoptime__departure_time__lte=(origin_time + 60),
                    gtfsstoptime__stop_id=origin_id)

            # If there's still nothing try checking for buses after midnight
            if origin_time and not trips:
                print("none found, trying after midnight")
                origin_time += 86400
                shape_id_queryset = None
                trips = GTFSTrip.objects.filter(
                    route__route_name=route_name,
                    calendar__start_date__lte=today,
                    calendar__end_date__gte=today,
                    gtfsstoptime__arrival_time__gte=(origin_time - 60),
                    gtfsstoptime__departure_time__lte=(origin_time + 60),
                    gtfsstoptime__stop_id=origin_id)

            if trips:
                for trip in trips:
                    stops = trip.gtfsstoptime_set.all()
                    print("full stops set")

                    # Get the stops sequence number for origin and desitination stops
                    origin_seq = stops.filter(
                        stop_id=origin_id).values("stop_sequence")
                    dest_seq = stops.filter(
                        stop_id=destination_id).values("stop_sequence")
                    print(origin_seq)
                    print(dest_seq)
                    # The stops we want will have a sequence number between the origin and destination stops
                    these_stops = stops.filter(stop_sequence__gte=origin_seq,
                                            stop_sequence__lte=dest_seq)

            # print(shape_id_queryset)

        if trips:
            
            for trip in trips:
                stops = trip.gtfsstoptime_set.all()
                print(stops.values("stop_id", "stop_sequence"))
                print(origin_id)
                print(destination_id)
                # Get the stops sequence number for origin and desitination stops
                origin_seq = stops.filter(
                    stop_id=origin_id).values("stop_sequence")
                dest_seq = stops.filter(
                    stop_id=destination_id).values("stop_sequence")
                print(origin_seq)
                print(dest_seq)
                # The stops we want will have a sequence number between the origin and destination stops
                these_stops = stops.filter(stop_sequence__gte=origin_seq,
                                           stop_sequence__lte=dest_seq)

                print(these_stops)
                # Get the list of plate codes and stop sequences
                these_stops_list = list(these_stops.values("stop_sequence",
                                                           plate_code=F("stop__plate_code"),
                                                           time=F("arrival_time"),
                                                           stop_name=F("stop__stop_name")))

                # append the stops to both lists
                if these_stops and these_stops_list not in stops_as_lists:
                    stop_query_set.append(these_stops)
                    stops_as_lists.append(these_stops_list)
            
        if not stops_as_lists:

            print("none found, going by route name")
            trips = None
            shape_id_queryset = GTFSTrip.objects.filter(
                route__route_name=route_name,
                calendar__start_date__lte=today,
                calendar__end_date__gte=today).values("shape_id").distinct().values_list('shape_id', flat=True)
            print(shape_id_queryset)

            # Get the list of stops for each shape_id
            for shape in shape_id_queryset:

                # Get all stops for this shape
                stops = self.stops_on_route(shape)
                
                # print(stops)
                # Get the stops sequence number for origin and desitination stops
                origin_seq = stops.filter(
                    stop_id=origin_id).values("stop_sequence")
                dest_seq = stops.filter(
                    stop_id=destination_id).values("stop_sequence")


                print(origin_seq)
                print(dest_seq)
                if origin_seq and dest_seq:
                    # The stops we want will have a sequence number between the origin and destination stops
                    these_stops = stops.filter(stop_sequence__gte=origin_seq,
                                            stop_sequence__lte=dest_seq)
                    print(these_stops)
                    # Get the list of plate codes and stop sequences
                    return [list(these_stops.values("stop_sequence",  stop_name=F("stop__stop_name"), plate_code=F("stop__plate_code"), shape_id=F("trip__shape_id")))]

                    # # append the stops to both lists
                    # if these_stops and these_stops_list not in stops_as_lists:
                    #     stop_query_set.append(these_stops)
                    #     stops_as_lists.append(these_stops_list)

        # Return stop objects or a list as needed
        if get_objects:
            print("ret")
            return stop_query_set
        else:
            print("returning from get stops between")
            print(stops_as_lists)
            return stops_as_lists

    def stops_on_route(self, shape_id):
        ''' Given a routeshape get all stops on the route'''

        trip = GTFSTrip.objects.filter(shape_id=shape_id).first()
        return trip.gtfsstoptime_set.all()

    def get_all_routes(self):
        today = datetime.datetime.today()
        trips = GTFSTrip.objects.filter(
            calendar__start_date__lte=today,
            calendar__end_date__gte=today).values(route_name=F("route__route_name"),
                                                  operator=F("route__agency__agency_name")).distinct()
        return trips


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
