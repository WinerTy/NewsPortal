from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.db.models import Q

def MainPage(request):
    return render(request, 'BD/MainPage.html', {'title': 'Главная страница'})

class NewsView():
    # Передача Содержания автора даты и тд
    @classmethod
    def ShowNews(cls, request):
        posts = Post.objects.all().order_by('-date')


        paginator = Paginator(posts, 10)
        page = request.GET.get('page')

        try:

            posts = paginator.page(page)

        except PageNotAnInteger:

            posts = paginator.page(1)

        except EmptyPage:

            posts = paginator.page(paginator.num_pages)

        return render(request, 'BD/MainPage.html', {'posts': posts})

    # Вызывает шаблон для страницы с Полной инфорпацией о любом посте
    @classmethod
    def Post_detal(cls, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        return render(request, 'BD/PostDetal.html', {'post': post})


    def ShowAllNews(request):
        posts = Post.objects.all().order_by('-date')

        return render(request, 'BD/AllNews.html', {'posts': posts})

class information():
    def get_date(self):
        return Post.objects.get('created')
    def get_title(self):
        return Post.objects.get('title')
    def get_author(self):
        return Post.objects.get('author')

class filter(information,ListView):
    def get_queryset(self):
        queryset = Post.objects.filter(
            Q(date__in=self.request.GET.getlist("-date"))|
            Q(title__in=self.request.GET.getlist("title"))|
            Q(author__in=self.request.GET.getlist("author"))
        )
        return queryset