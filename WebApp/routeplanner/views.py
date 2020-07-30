from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pyleapcard import *
import re
import requests
from .forms import leapCardForm


def home(request):
    # api key and url for weather data
    API = '83e8d16b48f83517a5d89158fc88656e'
    URL = "http://api.openweathermap.org/data/2.5/weather?q=Dublin,ie&appid=" + API
    try:
        city_weather = requests.get(url=URL).json()  # sends request to API and resturns weather data in Json
    except:
        print("Error, Weather Data Not Recieved")

    # weather information as dictionaryt to be included in context
    context = {"weather": {
        'temperature': int(city_weather['main']['temp'] - 273.15),
        'description': city_weather['weather'][0]['description'],
        'icon': city_weather['weather'][0]['icon']
    }}

    return render(request, 'routeplanner/home.html', context)


def journey(request, template_name="routeplanner/home.html"):
    return render(request, 'routeplanner/journey.html')


def stops(request):
    return render(request, 'routeplanner/stops.html')


def routes(request):
    return render(request, 'routeplanner/routes.html')


def leapcard(request):
    # simply return the leapcard form and pass the data
    form = leapCardForm()
    return render(request, 'routeplanner/leapcard.html', {'form': form})


@csrf_exempt
def leapinfo(request):
    if request.method == 'POST':
        # after getting username nad passrod from the form convert it to a string
        userinfo = str(request.body)

        # use regualr expression to get username and password
        pre_username = re.search(".+?(?=&password=)", userinfo).group(0)
        username = re.search("(?<=username=).[^']*", pre_username).group(0)
        password = re.search("(?<=password=).[^']*", userinfo).group(0)

        # pass the username and password to leapcard api
        session = LeapSession()

        try:
            # if the info is valid get the card overciew
            login_ok = session.try_login(username, password)
            overview = session.get_card_overview()

            # only extract card_label and balance
            card_info = {"Card ": vars(overview)['card_label'],
                         "Balance ": vars(overview)['balance']}

            # return them to the frontend
            return JsonResponse(card_info, safe=False)

        except Exception as e:
            # return error message if username and password is invalid
            error = "Error: Unable to retrieve Leap Card state."
            return JsonResponse(error, safe=False)


def realtimeInfo(request, stop_id):
    r = requests.get(f"https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid={stop_id}&format=json%27")
    return JsonResponse(r.text, safe=False)

# function to format api geocoordinates request to get lat and long of user-entered address
# def longlatsearch(request, address):
#     res = tuple(map(str, address.split(' ')))
#     if len(res)==1:
#         r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address={res[0]}&key=AIzaSyBavSlO4XStz2_RD_fUBGwm89mQwGwYUzA")
#     #address needs to be formatted with + between each word
#     else:
#         address = ''
#         for i in range(0,len(res)-2):
#             address += res[i]
#             address += '+'
#         address += res[-1]
#         r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address={address}&key=AIzaSyBavSlO4XStz2_RD_fUBGwm89mQwGwYUzA")
#     return JsonResponse(r.text, safe=False)
