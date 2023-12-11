from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def MainPage(request):
    return render(request, 'BD/MainPage.html', {'title': 'Главная страница'})

class NewsView():
    # Передача Содержания автора даты и тд
    @classmethod
    def ShowNews(cls, request):
        posts = Post.objects.all().order_by('-date')


        paginator = Paginator(posts, 6)
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

class Sorting():
    def knopka(request):
        sort_by = request.GET.get('sort', 'author')
        if sort_by == 'author':
            post = Post.objects.all().order_by('title')
        elif sort_by == 'title':
            post = Post.objects.all().order_by('author')
        elif sort_by == 'date':
            post = Post.objects.all().order_by('date')
        else:
            post = Post.objects.value_list('author', 'title', 'date')
        return render(request, 'BD/sort_post.html', {'post': post, 'sort_by': sort_by})