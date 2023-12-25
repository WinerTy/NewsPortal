from django.urls import path

from . import views

urlpatterns = [
    path('weather/test', views.get_weather, name='weather1')
]