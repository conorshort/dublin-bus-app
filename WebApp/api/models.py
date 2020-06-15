
from django.db import models



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


class GTFSRoute(models.Model):
    route_id = models.CharField(primary_key=True, max_length=50)
    route_name = models.CharField(max_length=20)

    class Meta:
        managed = True
        db_table = 'gtfs_routes'


class GTFSShapeManager(models.Manager):

    def get_shape_json_by_shape_id(self, shape_id):
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

    def update_all_shapes(self):
        import pandas as pd
        print("Getting data...")
        df = pd.read_csv(static("dublin_bus_gtfs/shapes.txt"))
        df_records = df.to_dict('records')

        print("Adding to db...")
        model_instances = [RouteShape(
            unique_point_id=f'{record["shape_id"]}-seq:{record["shape_pt_sequence"]}',
            shape_id=record["shape_id"],
            shape_pt_lat=record["shape_pt_lat"],
            shape_pt_lon=record["shape_pt_lon"],
            shape_pt_sequence=record["shape_pt_sequence"]
        ) for record in df_records]

        self.bulk_create(model_instances,
                         batch_size=100,
                         ignore_conflicts=True)
        print("Done")


class GTFSShape(models.Model):
    unique_point_id = models.CharField(primary_key=True, max_length=30)
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
        db_table = 'shapes'
        unique_together = (("shape_id", "shape_pt_sequence"),)












class GTFSStopTime(models.Model)
    class Meta:
            managed = True
            db_table = 'gtfs_stop_times'

class GTFSStop(models.Model)
    class Meta:
            managed = True
            db_table = 'gtfs_stops'


class GTFSTrip(models.Model)
    class Meta:
                managed = True
                db_table = 'gtfs_trips'
