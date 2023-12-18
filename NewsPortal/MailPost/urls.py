from django.urls import path

from .views import Subscriber



urlpatterns = [
    path('rolenews', Subscriber.get_role_news,name='rolenews'),
    path('rolearticle', Subscriber.get_role_article, name='rolearticle')
]