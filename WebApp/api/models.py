
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
    # Duplicate of stopid, can be deleted
    displaystopid = models.IntegerField(blank=True, null=True)
    # Very similar to fullname, can be deleted
    shortname = models.CharField(max_length=200, blank=True, null=True)
    shortnamelocalized = models.CharField(
        max_length=200, blank=True, null=True)
    fullname = models.CharField(
        max_length=200, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    lastupdated = models.DateField(blank=True, null=True)
    # constant value, can be deleted
    operator = models.CharField(max_length=20, blank=True, null=True)
    # constant value, can be deleted
    op_type = models.IntegerField(blank=True, null=True)
    routes = models.TextField(blank=True, null=True)

    # # Model manager
    # objects = BusStopManager()

    class Meta:
        # managed = True
        db_table = 'all_bus_stops'


class RouteShapeManager(models.Manager):

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
            shape_dist_traveled=record["shape_dist_traveled"]# Doesn't seem accurate or useful, can be deleted
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


class StopSequencesManager(models.Manager):
    ''' This class contains functions for dealing with and manipulating StopSequence'''

    def __format_sequences_csv(self, route_seq_csv):
        ''' Format a routesequencecsv for adding to the database '''
        import pandas as pd
        import numpy as np
        print("Reading csv...")
        df = pd.read_csv(route_seq_csv)

        print("Parsing data...")
        # We only want data for Dublin Bus
        df = df.copy().loc[df.Operator == "Dublin Bus"]
        df = df.drop(columns=['RouteData', "AtcoCode"])

        # Change HasPole to a boolean
        df.loc[df['HasPole'] == "Pole", "HasPole"] = 1
        df.loc[df['HasPole'] == "No Pole", "HasPole"] = 0
        df.loc[df['HasPole'] == "Unknown", "HasPole"] = None

        # Change HasShelter to a boolean
        df.loc[df['HasShelter'] == "Shelter", 'HasShelter'] = 1
        df.loc[df['HasShelter'] == "No Shelter", 'HasShelter'] = 0
        df.loc[df['HasShelter'] == "Unknown", 'HasShelter'] = None

        # Change Direction to DirectionInbound and make it a boolean
        df = df.rename(columns={'Direction': 'DirectionInbound'})
        df.loc[df['DirectionInbound'] == "Outbound", "DirectionInbound"] = 0
        df.loc[df['DirectionInbound'] == "Inbound", "DirectionInbound"] = 1

        # Replace NaN with None to keep django happy
        df = df.replace(np.nan, None)
        return df

    def update_all_routes(self):
        ''' update all route sequences from a route sequence csv '''
        import pandas as pd

        # TODO: decide where to put this file and update path
        route_seq_csv = "C:/Users/cls15/Google Drive/Comp Sci/Research Practicum/Code/dublin-bus-app/Models/Data Cleaning/routesequences.csv"

        #Load and parse the csv
        df = self.__format_sequences_csv(route_seq_csv)

        print("Adding to db...")

        # Make a list of StopSequence instances using the df
        stop_sequence_instances = [StopSequence(
            ID=row["ID"],
            shape_id=row["ShapeId"],
            operator=row["Operator"],
            stop_sequence=row["StopSequence"],
            route_name=row["RouteName"],
            direction_inbound=row["DirectionInbound"],
            plate_code=row["PlateCode"],
            short_common_name_en=row["ShortCommonName_en"],
            short_common_name_ga=row["ShortCommonName_ga"],
            has_pole=row["HasPole"],
            has_shelter=row["HasShelter"],
            carousel_type=row["CarouselType"],
            flag_data=row["FlagData"]
        ) for index, row in df.iterrows()]

        # Add them to the db
        self.bulk_create(stop_sequence_instances,
                        batch_size=100,
                        ignore_conflicts=True)
        print("Done")

class StopSequence(models.Model):
    ID = models.IntegerField(primary_key=True)
    shape_id = models.CharField(max_length=30)
    operator = models.CharField(max_length=50)
    stop_sequence = models.IntegerField()
    route_name = models.CharField(max_length=10)
    direction_inbound = models.BooleanField()
    plate_code = models.IntegerField(blank=True, null=True)
    short_common_name_en = models.CharField(
        max_length=100, blank=True, null=True)
    short_common_name_ga = models.CharField(
        max_length=100, blank=True, null=True)
    has_pole = models.BooleanField(blank=True, null=True)
    has_shelter = models.BooleanField(blank=True, null=True)
    carousel_type = models.CharField(max_length=100, blank=True, null=True)
    flag_data = models.CharField(max_length=100, blank=True, null=True)

    objects = StopSequencesManager()

    class Meta:
        managed = True
        db_table = 'stopsequences'
        unique_together = (("shape_id", "stop_sequence"),)

