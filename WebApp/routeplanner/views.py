from django.shortcuts import render
from django.http import HttpResponse
import requests
import json

dummy_bus_content = [
    {
        'route': '16',
        'from': 'Dublin Airport',
        'to': 'Ballinteer (Kingston)',
        'time': '06:45'
    },
    {
        'route': '41',
        'from': 'Lwr. Abbey St',
        'to': 'Swords Manor',
        'time': '15:55'
    }
]


def home(request):
    context = {
        'busses': dummy_bus_content
    }
    return render(request, 'routeplanner/home.html', context)

def journey(request):
    return render(request, 'routeplanner/journey.html')

def stops(request):

    URL = 'http://127.0.0.1:8000/api/stops'
    try:
        r = requests.get(URL, timeout=20)
    except requests.exceptions.RequestException as e:
        print("Something went wrong: could not connect to", URL)
        return render(request, 'routeplanner/stops.html', {})
    else:
        stops = json.loads(r.text)
        context = {
            'stops': stops
        }
        return render(request, 'routeplanner/stops.html', context)

def routes(request):
    return render(request, 'routeplanner/routes.html')

def leapcard(request):
    return render(request, 'routeplanner/leapcard.html')