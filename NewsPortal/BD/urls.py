from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page

from .views import (
    NewsView, PostInfo, FindPost, CreatePost, DeletePost, UpdatePost
)

urlpatterns = [
    path('main/', NewsView.as_view(), name='main'),
    path('news/', PostInfo.ShowAllNews, name='All_news'),
    path('news/<int:post_id>/', PostInfo.Post_detal, name='Post Details'),
    path('news/create/', login_required(CreatePost.create), name='create post'),
    path('news/<int:pk>/update/', UpdatePost.as_view(), name='update post'),
    path('news/<int:pk>/delete', DeletePost.as_view(), name='delete post'),
    path('search/', FindPost.Find, name='Find'),
    path('', include('avtorization.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
