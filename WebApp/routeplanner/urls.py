from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="routeplanner"),
    path('stops', views.stops, name="stops"),
    path('routes', views.routes, name="routes"),
    path('leapcard', views.leapcard, name="leapcard"),
]
