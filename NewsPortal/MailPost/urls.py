from django.urls import path, include, re_path

from .views import Subscriber


urlpatterns = [
    path('rolenews/', Subscriber.get_role_news,name='rolenews'),
    path('rolearticle/', Subscriber.get_role_article, name='rolearticle'),
    path('remrolenews/', Subscriber.remove_role_news, name='remrolenews'),
    path('remrolearticle/', Subscriber.remove_role_article, name='removerolearticle'),
    path('remroles/', Subscriber.remove_role_sub , name='remroles'),
]