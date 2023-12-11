from django.urls import path
from .views import NewsView, Sorting
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('main/', NewsView.ShowNews, name='main'),
    path('main/<int:post_id>/', NewsView.Post_detal, name='Post Details'),
    path('all_news/', NewsView.ShowAllNews, name='All_news'),
    path('filters/', Sorting.knopka, name='sortirovka'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)