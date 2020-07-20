from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from pprint import pprint
from pyleapcard import *
import re
from django.http import HttpResponse, JsonResponse
import requests
from dublin_bus.config import GOOGLE_DIRECTION_KEY
from .forms import leapCardForm

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


def journey(request, template_name="routeplanner/home.html"):
    
    return render(request, 'routeplanner/journey.html')

    # # If this is a POST request then process the Form data
    # if request.method == 'POST':
    #     # Create a form instance and populate it with data from the request (binding):
    #     form = JourneyPlannerForm(request.POST)

    #     # Check if the form is valid:
    #     if form.is_valid():

    #         print("is_valid")

    #         from_location = form.cleaned_data['from_location'] 
    #         to_location = form.cleaned_data['to_location']
    #         date = form.cleaned_data['date'] 
    #         time = form.cleaned_data['time'] 
    #         # api-endpoint 
    #         URL = "https://maps.googleapis.com/maps/api/directions/json"
            
            
    #         # defining a params dict for the parameters to be sent to the API 
    #         PARAMS = {'origin' : from_location,
    #                 'destination' : to_location,
    #                 'key' : GOOGLE_DIRECTION_KEY,
    #                 'transit_mode' : 'bus',
    #                 'mode' : 'transit'} 
            
    #         # sending get request and saving the response as response object 
    #         r = requests.get(url = URL, params = PARAMS) 
            
    #         # extracting data in json format 
    #         data = r.json() 
    #         # return render(request, 'routeplanner/journey.html',{'form': form,'result':data})
    #         print(data)
    #     # Create a response
    #     response = TemplateResponse(request, template_name, {'form': form,'result':'result'})
    #     return response
    #     # form = JourneyPlannerForm()
    #     # return render(request, 'routeplanner/journey.html', {'form': form})

    # else: 
    
        # form = JourneyPlannerForm()
        # return render(request, 'routeplanner/journey.html', {'form': form})
    

def stops(request):
    return render(request, 'routeplanner/stops.html')

def routes(request):
    return render(request, 'routeplanner/routes.html')

def leapcard(request):
    #simply return the leapcard form and pass the data 
    form = leapCardForm()
    return render(request, 'routeplanner/leapcard.html',{'form': form})

@csrf_exempt
def leapinfo(request):
    if request.method == 'POST':
        # after getting username nad passrod from the form convert it to a string
        userinfo=str(request.body)

        #use regualr expression to get username and password
        pre_username=re.search(".+?(?=&password=)",userinfo).group(0)
        username=re.search("(?<=username=).[^']*",pre_username).group(0)
        password=re.search("(?<=password=).[^']*",userinfo).group(0)

        #pass the username and password to leapcard api
        session = LeapSession()

        try:
            #if the info is valid get the card overciew
            login_ok = session.try_login(username, password)
            overview = session.get_card_overview()

            #only extract card_label and balance
            # card_info = {"Card ":vars(overview)['card_label'],
            # "Balance ":vars(overview)['balance']}
            resp="Card label: ",vars(overview)['card_label'],", "," balance: ",vars(overview)['balance']
            #return them to the frontend
            return HttpResponse(resp, content_type='application/json')

        except Exception as e:
            #return error message if username and password is invalid
            error="Error: Unable to retrieve Leap Card state"
            return HttpResponse(error, content_type='application/json')
            # return JsonResponse(error)
                        

def realtimeInfo(request, stop_id):
    r = requests.get(f"https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid={stop_id}&format=json%27")
    return JsonResponse(r.text, safe=False)


