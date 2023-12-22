
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group


from django.shortcuts import redirect




@login_required # Переделать
class Subscriber():
    def get_role_news(request):
        group = Group.objects.get(name='news')
        request.user.groups.add(group)
        return redirect('/main')

    def get_role_article(request):
        group = Group.objects.get(name='article')
        request.user.groups.add(group)
        return redirect('/main')

    def remove_role_news(request):
        group = Group.objects.get(name='news')
        request.user.groups.remove(group)
        return redirect('/main')

    def remove_role_article(request):
        group = Group.objects.get(name='article')
        request.user.groups.remove(group)
        return redirect('/main')

    def remove_role_sub(request):
        groups = Group.objects.filter(name__in=['article', 'news'])
        for group in groups:
            request.user.groups.remove(group)
        return redirect('/main')
