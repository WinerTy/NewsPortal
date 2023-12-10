from django.urls import path
from . import views
from .views import NewsView, filter
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('main/', views.MainPage, name='main'),
    path('news/', NewsView.ShowNews, name='news'),
    path('filter/', filter.get_queryset, name='filter'),
    path('news/<int:post_id>/', NewsView.Post_detal, name='Post Details')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)