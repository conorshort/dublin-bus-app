from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="routeplanner"),
    path('journey', views.journey, name="journey"),
    path('stops', views.stops, name="stops"),
    path('routes', views.routes, name="routes"),
    path('leapcard', views.leapcard, name="leapcard"),
    path('leapinfo', views.leapinfo, name="leapinfo"),
    path('favourite', views.favourite, name="favourite"),
    path('realtimeInfo/<str:stop_id>', views.realtimeInfo, name="realtimeInfo")
    # path('set_cookie', views.set_cookie, name="set_cookie"),
    # path('get_cookie', views.get_cookie, name="get_cookie")
]

