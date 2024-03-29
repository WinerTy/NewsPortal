from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DeleteView, UpdateView

from .models import Post, PostCategory, Category
from .forms import PostForm



def MainPage(request):
    return render(request, 'BD/MainPage.html', {'title': 'Главная страница'})

class NewsView(ListView):
    model = Post
    ordering = '-date'
    template_name = 'BD/MainPage.html'
    context_object_name = 'posts'
    paginate_by = 8
    def get_queryset(self):
        return super().get_queryset().order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = self.get_queryset()
        paginator = Paginator(posts, self.paginate_by)
        page = self.request.GET.get('page')

        try:

            posts = paginator.page(page)

        except PageNotAnInteger:

            posts = paginator.page(1)

        except EmptyPage:

            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts

        return context

    # Вызывает шаблон для страницы с Полной инфорпацией о любом посте

class PostInfo():
    @classmethod
    def Post_detal(cls, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        category = ', '.join(str(e) for e in PostCategory.objects.filter(post__id=post_id).values_list('category__name', flat=True))
        return render(request, 'BD/PostDetal.html', {'post': post, 'category': category})

    def ShowAllNews(request):
        posts = Post.objects.all().order_by('-date')
        paginator = Paginator(posts, 10)

        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:

            posts = paginator.page(1)
        except EmptyPage:

            posts = paginator.page(paginator.num_pages)

        return render(request, 'BD/AllNews.html', {'posts': posts})


class FindPost():
    def Find(request):
        search_author = request.GET.get('Find_author', '')
        search_title = request.GET.get('Find_title', '')
        search_date = request.GET.get('Find_date', '')
        posts = Post.objects.all()

        if search_author or search_title or search_date:
            if search_author:
                posts = posts.filter(author__username__icontains=search_author)

            if search_title:
                posts = posts.filter(title__icontains=search_title)

            if search_date:
                posts = posts.filter(date__date=search_date)
        else:
            posts = Post.objects.all()
        return render(request, 'BD/sort_post.html', {'posts': posts})


class CreatePost():
    def create(request):
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                form.save(request.user)
                return redirect('All_news')

        form = PostForm()

        posts = {
            'form': form,
        }
        return render(request, 'BD/create_post.html', posts)

class UpdatePost(UpdateView):
    model = Post
    template_name = 'BD/create_post.html'
    fields = ['title', 'text']

class DeletePost(DeleteView):
    model = Post
    success_url = '/news'
    template_name = 'BD/delete_post.html'



