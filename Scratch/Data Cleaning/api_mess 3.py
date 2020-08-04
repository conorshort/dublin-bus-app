import requests

r = requests.get(
    'https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid=184&format=json')

print(r.text)
