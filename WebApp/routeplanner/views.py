from django.shortcuts import render
from django.http import HttpResponse
from pprint import pprint
from pyleapcard import *

from .forms import leapCardForm

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
                # pprint(overview)
                cardInfo = 'Card:',vars(overview)['card_label'],'Balance: €',vars(overview)['balance']
                return render(request, 'routeplanner/leapcard.html',{'form': form,'Result':cardInfo})
                
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