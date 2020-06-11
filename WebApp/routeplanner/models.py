from django.db import models


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
                displaystopid=stop["displaystopid"],
                shortname=stop["shortname"],
                shortnamelocalized=stop["shortnamelocalized"],
                fullname=stop["fullname"],
                latitude=stop["latitude"],
                longitude=stop["longitude"],
                lastupdated=last_update_str,
                operator=stop["operators"][bac_idx]["name"],
                op_type=stop["operators"][bac_idx]["operatortype"],
                routes=stop["operators"][bac_idx]["routes"]
            ))

        # Add all BusStop instances to the DB
        self.bulk_create(
            bus_stops, batch_size=100, ignore_conflicts=True)
        print("Done")


class BusStop(models.Model):
    stopid = models.IntegerField(primary_key=True)
    displaystopid = models.IntegerField(blank=True, null=True) # Duplicate of stopid, can be deleted
    shortname = models.CharField(max_length=200, blank=True, null=True)  # Very similar to fullname, can be deleted
    shortnamelocalized = models.CharField(
        max_length=200, blank=True, null=True)
    fullname = models.CharField(
        max_length=200, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    lastupdated = models.DateField(blank=True, null=True)
    operator = models.CharField(max_length=20, blank=True, null=True)  # constant value, can be deleted
    op_type = models.IntegerField(blank=True, null=True)  # constant value, can be deleted
    routes = models.TextField(blank=True, null=True)

    # Model manager
    objects = BusStopManager()

    class Meta:
        managed = True
        db_table = 'all_bus_stops'


class RouteShapeManager(models.Manager):
    
    def get_shape_json_by_shape_id(self, shape_id):

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
        df = pd.read_csv(
            "C:/Users/cls15/Google Drive/Comp Sci/Research Practicum/Code/dublin-bus-app/Models/Data Cleaning/shapes.txt")
        df_records = df.to_dict('records')

        print("Adding to db...")
        model_instances = [RouteShape(
            unique_point_id=f'{record["shape_id"]}-seq:{record["shape_pt_sequence"]}',
            shape_id=record["shape_id"],
            shape_pt_lat=record["shape_pt_lat"],
            shape_pt_lon=record["shape_pt_lon"],
            shape_pt_sequence=record["shape_pt_sequence"],
            shape_dist_traveled=record["shape_dist_traveled"] # Doesn't seem accurate or useful, can be deleted
        ) for record in df_records]

        self.bulk_create(model_instances,
                         batch_size=100,
                         ignore_conflicts=True)
        print("Done")


class RouteShape(models.Model):
    unique_point_id = models.CharField(primary_key=True, max_length=30)
    shape_id = models.CharField(max_length=30)
    shape_pt_lat = models.FloatField(blank=True, null=True)
    shape_pt_lon = models.FloatField(blank=True, null=True)
    shape_pt_sequence = models.IntegerField()
    shape_dist_traveled = models.FloatField(blank=True, null=True) # Doesn't seem accurate or useful, can be deleted

    # Model manager
    objects = RouteShapeManager()

    def __repr__(self):
        return f'''Id: {self.shape_id};
                   Coords: {self.shape_pt_lat}, {self.shape_pt_lon};
                   Seq: {self.shape_pt_sequence}'''

    class Meta:
        managed = True
        db_table = 'routeshapes'
        unique_together = (("shape_id", "shape_pt_sequence"),)
