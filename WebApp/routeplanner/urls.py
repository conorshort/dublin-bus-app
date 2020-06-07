from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="routeplanner"),
    path('about', views.about, name="about"),
]
