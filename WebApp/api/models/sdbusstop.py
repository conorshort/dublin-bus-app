from django.db import models
from django.templatetags.static import static


# ===== Bus Stops obtained from Smart Dublin API =====


class SmartDublinBusStopManager(models.Manager):

    def get_nearest_id(self, latitude, longitude):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""select *, ST_Distance_Sphere(point ( %s ,  %s ),
                              point(longitude, latitude))
                        as distance_in_metres
                from sd_bus_stops
                order by distance_in_metres asc
                limit 1;""" % (longitude, latitude))
            result_list = []
            # There should only be one nearest stop
            for row in cursor.fetchall():
                return row[0]
        return None

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
            bus_stops.append(SmartDublinBusStop(
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
            bus_stops, batch_size=1000, ignore_conflicts=True)
        print("Done")


class SmartDublinBusStop(models.Model):
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
    objects = SmartDublinBusStopManager()

    class Meta:
        managed = True
        db_table = 'sd_bus_stops'
