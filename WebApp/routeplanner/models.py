from django.db import models
import requests
import pandas as pd
import json


class Cat(models.Model):
    idcat = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cat'


class BusStop(models.Model):
    stopid = models.IntegerField(primary_key=True)
    displaystopid = models.IntegerField(blank=True, null=True)
    shortname = models.CharField(max_length=200, blank=True, null=True)
    shortnamelocalized = models.CharField(
        max_length=200, blank=True, null=True)
    fullname = models.CharField(
        max_length=200, blank=True, null=True)
    fullnamelocalized = models.CharField(
        max_length=200, blank=True, null=True)
    latitude = models.IntegerField(blank=True, null=True)
    longitude = models.IntegerField(blank=True, null=True)
    lastupdated = models.DateField(blank=True, null=True)
    operator = models.CharField(max_length=20, blank=True, null=True)
    op_type = models.IntegerField(blank=True, null=True)
    routes = models.TextField(blank=True, null=True)

    @classmethod
    def update_all_stops():

        r = requests.get(
            'https://data.smartdublin.ie/cgi-bin/rtpi/busstopinformation?&format=json')

        stops_json = json.loads(r.text)

        stops = []
        for stop in stops_json["results"]:

            # Only add stops served by Dublin Bus ("bac")
            bac_idx = 0
            for op in stop["operators"]:
                if op["name"] == "bac":
                    break
                else:
                    bac_present += 1
            else:
                continue

            cls(
                stopid=stop["stopid"],
                displaystopid=stop["displaystopid"],
                shortname=stop["shortname"],
                shortnamelocalized=stop["shortnamelocalized"],
                fullname=stop["fullname"],
                fullnamelocalized=stop["fullnamelocalized"],
                latitude=stop["latitude"],
                longitude=stop["longitude"],
                lastupdated=stop["lastupdated"],
                operator=stop["operators"][bac_idx]["name"],
                op_type=stop["operators"][bac_idx]["operatortype"],
                routes=stop["operators"][bac_idx]["routes"]
            ).save()

    class Meta:
        managed = True
        db_table = 'all_bus_stops'
