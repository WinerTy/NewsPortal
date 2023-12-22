from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm
from BD.models import Author


@login_required
def profile(request):
    return render(request, 'avtorization/profile.html')


def add_to_group(request):
    if request.user.is_authenticated:
        group = Group.objects.get(name='author')
        request.user.groups.add(group)
        author = Author.objects.create(user=request.user, rating=0)
        author.save()
    return redirect('/main')



def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/signup.html', {'form': form})




