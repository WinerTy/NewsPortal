from django.contrib.auth.models import Group

from django.shortcuts import redirect

from BD.models import SubArticle, SubNews


class Subscriber():

    def get_role_news(request):
        if request.user.is_authenticated:
            group = Group.objects.get(name='news')
            request.user.groups.add(group)
            author = SubNews.objects.create(user=request.user)
            author.save()
        return redirect('/main')

    def get_role_article(request):
        if request.user.is_authenticated:
            group = Group.objects.get(name='article')
            request.user.groups.add(group)
            artilerole = SubArticle.objects.create(user=request.user)
            artilerole.save()
        return redirect('/main')
    def new_post(self):
        pass