from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests

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

def realtimeInfo(request, stop_id):
    r = requests.get(f"https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid={stop_id}&format=json%27")
    return JsonResponse(r.text, safe=False)
