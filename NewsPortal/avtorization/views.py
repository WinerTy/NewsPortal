from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

@login_required
def profile(request):
    return render(request, 'avtorization/profile.html')


def add_to_group(request):
    if request.user.is_authenticated:
        group = Group.objects.get(name='author')
        request.user.groups.add(group)
    return redirect('/main')