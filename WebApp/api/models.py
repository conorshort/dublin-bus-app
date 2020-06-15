
from django.db import models
from django.templatetags.static import static


# ===== Bus Stops obtained from Smart Dublin API =====
class BusStopManager(models.Manager):

    def __get_all_bus_stop_data(self):
        ''' Connect to smartdublin api and return a JSON of all bus stops '''

        import requests
        import json

        print("Getting data...")

        all_stops_URL = 'https://data.smartdublin.ie/cgi-bin/rtpi/busstopinformation?&format=json'

        try:
            r = requests.get(all_stops_URL, timeout=20)
        except requests.exceptions.RequestException as e:
            print("Something went wrong: could not connect to", all_stops_URL)
            return None
        else:
            print("Data obtained.")
            return json.loads(r.text)["results"]

    def __format_date_for_django(self, date_str):
        ''' Format a date-time str from smartdublin API for use in Django model'''
        from datetime import datetime

        date_obj = datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")
        return date_obj.strftime("%Y-%m-%d")

    def update_all_stops(self):
        ''' Find all Dublin Bus stops currently in use and update the database '''
        stops_json = self.__get_all_bus_stop_data()

        print("Adding to db...")
        bus_stops = []
        for stop in stops_json:

            # Each stop can be served by one or more operators
            # Only add stops and routes served by Dublin Bus ("bac")
            bac_idx = 0
            for op in stop["operators"]:
                if op["name"] == "bac":
                    break
                else:
                    bac_idx += 1
            else:
                continue

            last_update_str = self.__format_date_for_django(
                stop["lastupdated"])

            # Make an instance of BusStop
            bus_stops.append(BusStop(
                stopid=stop["stopid"],
                shortnamelocalized=stop["shortnamelocalized"],
                fullname=stop["fullname"],
                latitude=stop["latitude"],
                longitude=stop["longitude"],
                lastupdated=last_update_str,
                routes=stop["operators"][bac_idx]["routes"]
            ))

        # Add all BusStop instances to the DB
        self.bulk_create(
            bus_stops, batch_size=100, ignore_conflicts=True)
        print("Done")


class BusStop(models.Model):
    stopid = models.IntegerField(primary_key=True)
    shortnamelocalized = models.CharField(
        max_length=200, blank=True, null=True)
    fullname = models.CharField(
        max_length=200, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    lastupdated = models.DateField(blank=True, null=True)
    routes = models.TextField(blank=True, null=True)

    # Model manager
    objects = BusStopManager()

    class Meta:
        managed = True
        db_table = 'bus_stops'


# ========================================================================================
# ========================================================================================
# Models for GTFS data found here https://transitfeeds.com/p/transport-for-ireland/782/latest



# ===== ROUTE =====
class GTFSRouteManager(models.Manager):
    def update_all(self):
        import pandas as pd
        print("Getting data...")
        df = pd.read_csv("api/static/api/dublin_bus_gtfs/routes.txt")
        df_records = df.to_dict('records')

        print("Adding to db...")
        model_instances = [GTFSRoute(
            route_id=record["route_id"],
            route_name=record["route_short_name"],
        ) for record in df_records]

        self.bulk_create(model_instances,
                         batch_size=10000,
                         ignore_conflicts=True)
        print("Done")


class GTFSRoute(models.Model):
    route_id = models.CharField(primary_key=True, max_length=50)
    route_name = models.CharField(max_length=20)

    objects = GTFSRouteManager()

    class Meta:
        managed = True
        db_table = 'gtfs_routes'

# ===== SHAPE =====


class GTFSShapeManager(models.Manager):

    def get_json_by_id(self, shape_id):
        ''' Take a shape_id and return a dict containing a list of its lats and'''
        shape = RouteShape.objects.filter(shape_id=shape_id)
        num_points = len(shape)
        shape_dict = {"shape_id": shape[0].shape_id,
                      "points": [None] * num_points
                      }
        for point in shape:
            pt_seq = point.shape_pt_sequence
            shape_dict["points"][pt_seq - 1] = {"lat": point.shape_pt_lat,
                                                "lon": point.shape_pt_lon}
        return shape_dict

    def update_all(self):
        import pandas as pd
        print("Getting data...")
        df = pd.read_csv("api/static/api/dublin_bus_gtfs/shapes.txt")
        df_records = df.to_dict('records')

        print("Adding to db...")
        shape_instances = []
        for record in df_records:
            shape_instances.append(GTFSShape(
                unique_point_id=f'{record["shape_id"]}:{record["shape_pt_sequence"]}',
                shape_id=record["shape_id"],
                shape_pt_lat=record["shape_pt_lat"],
                shape_pt_lon=record["shape_pt_lon"],
                shape_pt_sequence=record["shape_pt_sequence"]
            ))

        self.bulk_create(shape_instances,
                         batch_size=10000,
                         ignore_conflicts=True)
        print("\nDone")


class GTFSShape(models.Model):
    unique_point_id = models.CharField(primary_key=True, max_length=70)
    shape_id = models.CharField(max_length=30)
    shape_pt_lat = models.FloatField(blank=True, null=True)
    shape_pt_lon = models.FloatField(blank=True, null=True)
    shape_pt_sequence = models.IntegerField()

    # Model manager
    objects = GTFSShapeManager()

    def __repr__(self):
        return f'''Id: {self.shape_id};
                   Coords: {self.shape_pt_lat}, {self.shape_pt_lon};
                   Seq: {self.shape_pt_sequence}'''

    class Meta:
        managed = True
        db_table = 'gtfs_shapes'
        unique_together = (("shape_id", "shape_pt_sequence"),)


class GTFSStopTimeManager(models.Manager):

    def __time_to_secs(self, time):
        hrs, mins, secs = time.split(":")
        hrs_to_secs = int(hrs) * 3600
        mins_to_secs = int(mins) * 60
        return hrs_to_secs + mins_to_secs + int(secs)

    def update_all(self):
        import pandas as pd
        print("Getting data...")
        df = pd.read_csv("api/static/api/dublin_bus_gtfs/stop_times.txt")
        df_records = df.to_dict('records')

        print("Adding to db...")
                
        stop_time_instances = []
        for record in df_records:
            stop_time_instances.append(GTFSStopTime(
                unique_trip_id=f'{record["trip_id"]}:{record["stop_sequence"]}',
                trip_id=record["trip_id"],
                arrival_time=self.__time_to_secs(record["arrival_time"]),
                departure_time=self.__time_to_secs(record["depart ure_time"]),
                stop_id=record["stop_id"],
                stop_sequence=record["stop_sequence"],
                stop_headsign=record["stop_headsign"]
            ))

        self.bulk_create(stop_time_instances,
                         batch_size=10000,
                         ignore_conflicts=True)
        print("Done")


class GTFSStopTime(models.Model):
    unique_trip_id = models.CharField(primary_key=True, max_length=50)
    trip_id = models.CharField(max_length=50)
    arrival_time = models.IntegerField(blank=True, null=True)
    departure_time = models.IntegerField(blank=True, null=True)
    stop_id = models.CharField(max_length=50)
    stop_sequence = models.IntegerField()
    stop_headsign = models.CharField(max_length=200)

    # Model manager
    objects = GTFSStopTimeManager()

    class Meta:
        managed = True
        db_table = 'gtfs_stop_times'


class GTFSTripManager(models.Manager):

    def update_all(self):
        import pandas as pd
        print("Getting data...")
        df = pd.read_csv("api/static/api/dublin_bus_gtfs/trips.txt")
        df_records = df.to_dict('records')

        print("Adding to db...")
        trip_instances = []
        for i, record in enumerate(df_records):
            if i %100 == 0:
                print(i)
            trip_instances.append(GTFSTrip(
                route_id=record["route_id"],
                service_id=record["service_id"],
                trip_id=record["trip_id"],
                shape_id=record["shape_id"],
                trip_headsign=record["trip_headsign"],
                direction_id=record["direction_id"]
            ))

        self.bulk_create(trip_instances,
                         batch_size=10000,
                         ignore_conflicts=True)
        print("\nDone")



class GTFSTrip(models.Model):
    route_id = models.CharField(max_length=70)
    service_id = models.CharField(max_length=70)
    trip_id = models.CharField(primary_key=True, max_length=70)
    shape_id = models.CharField(max_length=70)
    trip_headsign = models.CharField(max_length=200)
    direction_id = models.IntegerField()

    # Model manager
    objects = GTFSTripManager()

    class Meta:
        managed = True
        db_table = 'gtfs_trips'
