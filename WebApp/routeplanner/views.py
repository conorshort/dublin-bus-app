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
API = '83e8d16b48f83517a5d89158fc88656e'
URL = "http://api.openweathermap.org/data/2.5/weather?q=Dublin,ie&appid=" + API
try:
    city_weather = requests.get(url=URL).json() #sends request to API and resturns weather data in Json
except:
    print("Error, Weather Data Not Recieved")        

weather = {
    'temperature' : int(city_weather['main']['temp'] - 273.15),
    'description' : city_weather['weather'][0]['description'],
    'icon' : city_weather['weather'][0]['icon']
}

def home(request):
    context = {
        'busses': dummy_bus_content,
        'weather': weather
    }
   
    return render(request, 'routeplanner/home.html', context)


def journey(request):
    return render(request, 'routeplanner/journey.html')

def stops(request):

    context = {
            'weather': weather,
            'title':'stops'
        }

    return render(request, 'routeplanner/stops.html', context)

def routes(request):
    context = {
            'weather': weather,
            'title':'stops'
        }
    return render(request, 'routeplanner/routes.html', context)

def leapcard(request):
    context = {
            'weather': weather,
            'title':'stops'
        }
    return render(request, 'routeplanner/leapcard.html', context,)

  