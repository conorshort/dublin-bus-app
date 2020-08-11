from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf.urls import include
from .views import SmartDublinBusStopViewSet, GTFSRouteViewSet, GTFSShapeViewSet, GTFSStopTimeViewSet, GTFSTripViewSet, realtimeInfo, direction

router = routers.DefaultRouter()
router.register('stops', SmartDublinBusStopViewSet)
router.register('routes', GTFSRouteViewSet)
router.register('shapes', GTFSShapeViewSet)
router.register('stoptime', GTFSStopTimeViewSet)
router.register('trips', GTFSTripViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('realtimeInfo/<str:stop_id>', realtimeInfo, name="realtimeInfo"),
    path('direction', direction, name="direction"),
]
