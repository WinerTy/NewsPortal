from django.urls import path
from .views import NewsView , PostInfo, Test1
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('main/', NewsView.as_view(), name='main'),
    path('main/<int:post_id>/', PostInfo.Post_detal, name='Post Details'),
    path('all_news/', PostInfo.ShowAllNews, name='All_news'),
    path('search/', Test1.test, name='Find'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)