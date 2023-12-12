from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import PostForm
from django.urls import reverse
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
        return render(request, 'BD/PostDetal.html', {'post': post})

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
        search_title = request.GET.get('Find_title','')
        search_date = request.GET.get('Find_date', '')
        posts = Post.objects.all()


        if search_author or search_title or search_date:
            if search_author:
                posts = posts.filter(author__user__username__icontains=search_author) # НЕ РАБОТЕТ

            if search_title:
                posts = posts.filter(title__contains=search_title)

            if search_date:
                posts = posts.filter(date__date=search_date)
            else:
                posts = Post.objects.all()
        else:
            posts = Post.objects.all()
        return render(request, 'BD/sort_post.html', {'posts': posts})


class CreatePost():
    def create(request):
        errors = ''
        if request.method == 'POST':
            form = PostForm(request.POST)
            print(form)
            if form.is_valid():
                print(form)
                form.save()
                return redirect('All_news')
            else:
                errors = 'Неверно заполнена'
                print(form)

        form = PostForm()
        print(form)

        posts = {
            'form': form,
            'errors': errors,
        }
        print(posts)
        return render(request, 'BD/create_post.html', posts)



class UpdatePost(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'BD/update_post.html'

class DeletePost(DeleteView):
    model = Post
    form_class = PostForm
    template_name = 'BD/delete_post.html'

    def get_success_url(self):
        return reverse('All_news', kwargs={''})