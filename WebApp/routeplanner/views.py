from django.shortcuts import render
from django.http import HttpResponse
import requests


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

    context = {
        'busses': dummy_bus_content,
        'weather': weather
    }
   

    return render(request, 'routeplanner/home.html', context)

def stops(request):
    return render(request, 'routeplanner/stops.html', {'title' : 'Stops'} )

def routes(request):
    return render(request, 'routeplanner/routes.html', {'title' : 'Routes'} )

def leapcard(request):
    return render(request, 'routeplanner/leapcard.html', {'title' : 'Leapcard'})

  