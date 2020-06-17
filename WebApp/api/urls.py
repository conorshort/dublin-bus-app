from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf.urls import include
from .views import BusStopViewSet, GTFSRouteViewSet, GTFSShapeViewSet, GTFSStopTimeViewSet, GTFSTripViewSet

router = routers.DefaultRouter()
router.register('stops', BusStopViewSet)
router.register('routes', GTFSRouteViewSet)
router.register('shapes', GTFSShapeViewSet)
router.register('stoptime', GTFSStopTimeViewSet)
router.register('trips', GTFSTripViewSet)


urlpatterns = [
    path('', include(router.urls)),
]