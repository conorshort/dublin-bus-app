from django.shortcuts import render
from django.http import HttpResponse
import requests
import json



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

]

#api key and url for weather data
API = '83e8d16b48f83517a5d89158fc88656e'
URL = "http://api.openweathermap.org/data/2.5/weather?q=Dublin,ie&appid=" + API
try:
    city_weather = requests.get(url=URL).json() #sends request to API and resturns weather data in Json
except:
    print("Error, Weather Data Not Recieved")        

#weather information as dictionaryt to be included in context
weather = {
    'temperature' : int(city_weather['main']['temp'] - 273.15),
    'description' : city_weather['weather'][0]['description'],
    'icon' : city_weather['weather'][0]['icon']
}


    context = {
        'weather': weather
    }
   
    return render(request, 'routeplanner/home.html', context)


def journey(request):
    return render(request, 'routeplanner/journey.html')

def stops(request):
    return render(request, 'routeplanner/stops.html')

def routes(request):
    return render(request, 'routeplanner/routes.html')

def leapcard(request):
    return render(request, 'routeplanner/leapcard.html')

  