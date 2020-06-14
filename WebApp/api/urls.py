from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf.urls import include
from .views import BusStopViewSet

router = routers.DefaultRouter()
router.register('stops', BusStopViewSet)

urlpatterns = [
    path('', include(router.urls)),
]