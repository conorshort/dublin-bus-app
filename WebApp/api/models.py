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
# Models to store the GTFS data found here https://transitfeeds.com/p/transport-for-ireland/782/latest


# =================== Manager for all GTFS classes ===================
# Includes a method that will read from a class's associated
# text file and add it to the db. Can be called with
# <gtfs-class>.objects.update_all()
class GTFSManager(models.Manager):

    def update_all(self):
        ''' Read data from a text file and import to mysql
        The text file is found as a class variable in each GTFS class'''
        import pandas as pd
        print("Getting data...")
        df = pd.read_csv(self.model._text_file)
        df_records=df.to_dict('records')

        print("Creating instances...")
        self.all().delete()
        model_instances = []
        for i, record in enumerate(df_records):
            gtfs_instance = self.model.from_dict(record)
            model_instances.append(gtfs_instance)
            if i % 10000 == 0:
                print(f"Adding entries up to {i} to db...")
                self.bulk_create(model_instances)
                model_instances = []
        self.bulk_create(model_instances)
        print("Done")


class AbstractGTFS(models.Model):
    ''' Abstract class that all GTFS classes inherit from
    Sets the model manager for each class to GTFSManager'''
    objects = GTFSManager()

    class Meta:
        abstract = True
    
    @classmethod
    def from_dict(cls, gtfs_dict):
        ''' Create an instance of a class from a dictionary
        If a class includes a _proc_func runs the dictionary
        throught that first '''

        # Create an instance of the class
        gtfs_instance = cls()

        # Alter the dictionary with _proc_func if found
        proc_func = getattr(gtfs_instance, "_proc_func", None)
        if proc_func:
            gtfs_dict = proc_func(gtfs_dict)
        
        # Loop through the dict and set the instance values
        for key, val in gtfs_dict.items():
            if key in dir(gtfs_instance):
                setattr(gtfs_instance, key, val)
        return gtfs_instance



# =================== ROUTE ===================

class GTFSRoute(AbstractGTFS):
    route_id=models.CharField(primary_key=True, max_length=50)
    route_name=models.CharField(max_length=20)

    _text_file = "api/static/api/dublin_bus_gtfs/routes.txt"

    def _proc_func(self, route_dict):
        route_dict["route_name"] = route_dict["route_short_name"]
        return route_dict

    def __repr__(self):
        return self.route_id + " " + self.route_name

    objects = models.Manager()

    class Meta:
        managed=True
        db_table='gtfs_routes'



# =================== SHAPE ===================

# ===== Shape Manager=====
class GTFSShapeManager(models.Manager):

    def get_json_by_id(self, shape_id):
        ''' Take a shape_id and return a dict containing a list of its lats and'''
        shape = GTFSShape.objects.filter(shape_id=shape_id)
        num_points=len(shape)
        shape_dict={"shape_id": shape[0].shape_id,
                      "points": [None] * num_points
                      }
        for point in shape:
            pt_seq=point.shape_pt_sequence
            shape_dict["points"][pt_seq - 1]={"lat": point.shape_pt_lat,
                                                "lon": point.shape_pt_lon}
        return shape_dict


# ===== Shape Model =====
class GTFSShape(AbstractGTFS):
    unique_point_id=models.CharField(primary_key=True, max_length=70)
    shape_id=models.CharField(max_length=30)
    shape_pt_lat=models.FloatField(blank=True, null=True)
    shape_pt_lon=models.FloatField(blank=True, null=True)
    shape_pt_sequence=models.IntegerField()

    # Model manager
    objects=GTFSShapeManager()

    _text_file = "api/static/api/dublin_bus_gtfs/shapes.txt"

    def _proc_func(self, shape_dict):
        shape_dict["unique_point_id"] = f'{shape_dict["shape_id"]}:{shape_dict["shape_pt_sequence"]}'
        return shape_dict

    def __repr__(self):
        return f'''Id: {self.shape_id};
                   Coords: {self.shape_pt_lat}, {self.shape_pt_lon};
                   Seq: {self.shape_pt_sequence}'''

    class Meta:
        managed=True
        db_table='gtfs_shapes'
        unique_together=(("shape_id", "shape_pt_sequence"),)

        
# =================== STOP TIMES ===================

class GTFSStopTime(AbstractGTFS):
    unique_trip_id=models.CharField(primary_key=True, max_length=50)
    trip_id=models.CharField(max_length=50)
    arrival_time = models.IntegerField(blank=True, null=True)
    departure_time=models.IntegerField(blank=True, null=True)
    stop_id=models.CharField(max_length=50)
    stop_sequence=models.IntegerField()
    stop_headsign=models.CharField(max_length=200)



    _text_file = "api/static/api/dublin_bus_gtfs/stop_times.txt"

    def __time_to_secs(self, time):
        hrs, mins, secs = time.split(":")
        hrs_to_secs = int(hrs) * 3600
        mins_to_secs = int(mins) * 60
        return hrs_to_secs + mins_to_secs + int(secs)

    def _proc_func(self, stop_time_dict):
        stop_time_dict["unique_trip_id"] = f'{stop_time_dict["trip_id"]}:{stop_time_dict["stop_sequence"]}'
        stop_time_dict["arrival_time"] = self.__time_to_secs(stop_time_dict["arrival_time"])
        stop_time_dict["departure_time"] = self.__time_to_secs(stop_time_dict["departure_time"])
        return stop_time_dict

    class Meta:
        managed=True
        db_table='gtfs_stop_times'
        
        
        
# =================== TRIPS ===================
class GTFSTrip(AbstractGTFS):
    route_id = models.CharField(max_length=70)
    service_id=models.CharField(max_length=70)
    trip_id=models.CharField(primary_key=True, max_length=70)
    shape_id=models.CharField(max_length=70)
    trip_headsign=models.CharField(max_length=200)
    direction_id=models.IntegerField()

    _text_file = "api/static/api/dublin_bus_gtfs/trips.txt"

    class Meta:
        managed=True
        db_table='gtfs_trips'

