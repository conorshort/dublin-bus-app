from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from pprint import pprint
from pyleapcard import *
import re
from django.http import HttpResponse, JsonResponse
import requests


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





def journey(request):
    return render(request, 'routeplanner/journey.html')




def stops(request):
    return render(request, 'routeplanner/stops.html')



def routes(request):
    return render(request, 'routeplanner/routes.html')

# @csrf_exempt
def leapcard(request):
    # if request.method == 'POST':
    #     print('hi-----1')
    #     form = leapCardForm(request.POST)

    #     if form.is_valid():
    #         print('hi-----')

    #         username = form.cleaned_data['username'] 
    #         password = form.cleaned_data['password']
    #         print('asdfasdf')
    #         login_url="https://www.leapcard.ie/en/login.aspx"
    #         session = LeapSession()

    #         # form = leapCardForm() 
            
    #         try:
    #             print('1234345345345')
    #             login_ok = session.try_login(username, password)
    #             overview = session.get_card_overview()

    #             card_info = {"card":vars(overview)['card_label'],
    #                         "balance":vars(overview)['balance']}

    #             # return render(request, 'routeplanner/leapcard.html',{'form': form,'result':card_info})
    #             # return JsonResponse()
    #             print('hi')
    #             return JsonResponse(card_info, safe=False)
    #             # return render(request, 'routeplanner/leapcard.html',{'form': form,'Result':error})

    #         except Exception as e:

    #             print("leapcard.ie | href="+login_url)
    #             error="Error: Unable to retrieve Leap Card state."
    #             return JsonResponse(error, safe=False)
    #             # return render(request, 'routeplanner/leapcard.html',{'form': form,'Result':error})
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

@csrf_exempt
def leapinfo(request):

    if request.method == 'POST':
        # after getting username nad passrod from the form convert it to a string
        userinfo=str(request.body)

        #use regualr expression to get username and password
        pre_username=re.search(".+?(?=&password=)",userinfo).group(0)
        username=re.search("(?<=username=).[^']*",pre_username).group(0)
        password=re.search("(?<=password=).[^']*",userinfo).group(0)


        login_url="https://www.leapcard.ie/en/login.aspx"
        #pass the username and password to leapcard api
        session = LeapSession()

        
        try:
            #if the info is valid get the card overciew
            login_ok = session.try_login(username, password)
            overview = session.get_card_overview()

            #only extract card_label and balance
            card_info = {"card":vars(overview)['card_label'],
                        "balance":vars(overview)['balance']}
            
            #return them to the frontend
            return JsonResponse(card_info, safe=False)
        
        except Exception as e:
            #return error message if username and password is invalid
            print("leapcard.ie | href="+login_url)
            error="Error: Unable to retrieve Leap Card state. Please visit "+login_url
            return JsonResponse(error, safe=False)
                        

def realtimeInfo(request, stop_id):
    r = requests.get(f"https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid={stop_id}&format=json%27")
    return JsonResponse(r.text, safe=False)
