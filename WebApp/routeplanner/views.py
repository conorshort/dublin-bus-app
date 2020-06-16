from django.shortcuts import render
from django.http import HttpResponse
import requests
import json

def home(request):
    return render(request, 'routeplanner/home.html')

def journey(request):
    return render(request, 'routeplanner/journey.html')

def stops(request):
    return render(request, 'routeplanner/stops.html')

def routes(request):
    return render(request, 'routeplanner/routes.html')

def leapcard(request):
    return render(request, 'routeplanner/leapcard.html')