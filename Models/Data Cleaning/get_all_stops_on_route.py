import requests
import pandas as pd
import json

r = requests.get(
    'https://data.smartdublin.ie/cgi-bin/rtpi/busstopinformation?&format=json')

t = json.loads(r.text)

stops = []
for stop in t["results"]:
    bac_idx = 0
    bac_present = False
    for op in stop["operators"]:
        if op["name"] == "bac":
            bac_present = True
            break
        else:
            print("inc", bac_idx)
            bac_present += 1
    else:
        continue


    stops.append({
        "stopid": stop["stopid"],
        "displaystopid": stop["displaystopid"],
        "shortname": stop["shortname"],
        "shortnamelocalized": stop["shortnamelocalized"],
        "fullname": stop["fullname"],
        "fullnamelocalized": stop["fullnamelocalized"],
        "latitude": stop["latitude"],
        "longitude": stop["longitude"],
        "lastupdated": stop["lastupdated"],
        "operator": stop["operators"][bac_idx]["name"],
        "op_type": stop["operators"][bac_idx]["operatortype"],
        "routes": stop["operators"][bac_idx]["routes"]
    })



