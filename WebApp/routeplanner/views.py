from django.shortcuts import render
from django.http import HttpResponse

from pprint import pprint
from pyleapcard import *

from django.http import HttpResponse, JsonResponse
import requests

from dublin_bus.config import GOOGLE_DIRECTION_KEY


from .forms import leapCardForm, JourneyPlannerForm


def home(request):
    #api key and url for weather data
    API = '83e8d16b48f83517a5d89158fc88656e'
    URL = "http://api.openweathermap.org/data/2.5/weather?q=Dublin,ie&appid=" + API
    try:
        city_weather = requests.get(url=URL).json() #sends request to API and resturns weather data in Json
    except:
        print("Error, Weather Data Not Recieved")        

    #weather information as dictionaryt to be included in context
    context = {"weather": {
        'temperature' : int(city_weather['main']['temp'] - 273.15),
        'description' : city_weather['weather'][0]['description'],
        'icon' : city_weather['weather'][0]['icon']
    }}

    
    return render(request, 'routeplanner/home.html', context)





def journey(request):
    
    print("request", request)
    # If this is a POST request then process the Form data
    if request.method == "POST":
        print("postttt")
        # # Create a form instance and populate it with data from the request (binding):
        # form = JourneyPlannerForm(request.POST)

        # # Check if the form is valid:
        # if form.is_valid():

        #     print("is_valid")

        #     from_location = form.cleaned_data['from_location'] 
        #     to_location = form.cleaned_data['to_location']
        #     date = form.cleaned_data['date'] 
        #     time = form.cleaned_data['time'] 
        #     # api-endpoint 
        #     URL = "https://maps.googleapis.com/maps/api/directions/json"
            
            
        #     # defining a params dict for the parameters to be sent to the API 
        #     PARAMS = {'origin' : from_location,
        #             'destination' : to_location,
        #             'key' : GOOGLE_DIRECTION_KEY,
        #             'transit_mode' : 'bus',
        #             'mode' : 'transit'} 
            
        #     # sending get request and saving the response as response object 
        #     r = requests.get(url = URL, params = PARAMS) 
            
        #     # extracting data in json format 
        #     data = r.json() 
        #     print(data)

    if request.method == "GET": 
        print("gettttt")
    
    form = JourneyPlannerForm()
    return render(request, 'routeplanner/journey.html', {'form': form})




def stops(request):
    return render(request, 'routeplanner/stops.html')



def routes(request):
    return render(request, 'routeplanner/routes.html')






def leapcard(request):

    if request.method == 'POST':
        form = leapCardForm(request.POST)
        if form.is_valid():
            #      leap = {
            #     'leapInfo': leap_card_content
            # }   
            username = form.cleaned_data['username'] 
            password = form.cleaned_data['password']

            login_url="https://www.leapcard.ie/en/login.aspx"
            session = LeapSession()

            form = leapCardForm() 
            
            try:
                login_ok = session.try_login(username, password)
                overview = session.get_card_overview()

                card_info = {"card":vars(overview)['card_label'],
                            "balance":vars(overview)['balance']}

                return render(request, 'routeplanner/leapcard.html',{'form': form,'result':card_info})
                
            except Exception as e:
                print("x")
                print("---")
                print("Error: Unable to retrieve Leap Card state.")
                print("---")
                print("leapcard.ie | href="+login_url)
                error="Error: Unable to retrieve Leap Card state."
                return render(request, 'routeplanner/leapcard.html',{'form': form,'Result':error})
                    
    form = leapCardForm()

    return render(request, 'routeplanner/leapcard.html',{'form': form})


    
leap_card_content = [
    {
        'a': 'Error: Unable to retrieve Leap Card state.',
        'b': 'leapcard.ie | href="https://www.leapcard.ie/en/login.aspx"',

    },
    # {
    #     'route': '41',
    #     'from': 'Lwr. Abbey St',
    #     'to': 'Swords Manor',
    #     'time': '15:55'
    # }
]






def realtimeInfo(request, stop_id):
    r = requests.get(f"https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid={stop_id}&format=json%27")
    return JsonResponse(r.text, safe=False)
