from django.urls import path
from .views import Test


urlpatterns = [
    path('register/', Test.test, name='registration'),
]