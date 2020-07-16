from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="routeplanner"),
    path('journey', views.journey, name="journey"),
    path('stops', views.stops, name="stops"),
    path('routes', views.routes, name="routes"),

    path('leapcard', views.leapcard, name="leapcard"),
    path('leapinfo', views.leapinfo, name="leapinfo"),
    path('realtimeInfo/<str:stop_id>', views.realtimeInfo, name="realtimeInfo"),

