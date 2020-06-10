from django.shortcuts import render
from django.http import HttpResponse


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

def stops(request):
    return render(request, 'routeplanner/stops.html')

def routes(request):
    return render(request, 'routeplanner/routes.html')

def leapcard(request):
    return render(request, 'routeplanner/leapcard.html')