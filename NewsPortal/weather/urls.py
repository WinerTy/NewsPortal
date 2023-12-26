from django.urls import path

from . import views

urlpatterns = [
    path('get_weather/', views.get_weather, name='weather1')
]