from . import views
from django.urls import path, include
from allauth.account import views as allauth_views
from .views import ProfileView


urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('login/', allauth_views.login, name='account_login'),
    path('logout/', allauth_views.logout, name='account_logout'),
    path('signup/', allauth_views.signup, name='account_signup'),
    path('password/reset/', allauth_views.password_reset, name='account_reset_password'),
    path('password/change/', allauth_views.password_change, name='account_change_password'),
    path('profile/', ProfileView.profile, name='profile'),
]