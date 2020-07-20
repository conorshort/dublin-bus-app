from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="routeplanner"),
    path('journey', views.journey, name="journey"),
    path('stops', views.stops, name="stops"),
    path('routes', views.routes, name="routes"),
    path('leapcard', views.leapcard, name="leapcard"),
    path('realtimeInfo/<str:stop_id>', views.realtimeInfo, name="realtimeInfo"),
    path('longlatsearch/<str:address>', views.longlatsearch, name='longlatsearch')
]
