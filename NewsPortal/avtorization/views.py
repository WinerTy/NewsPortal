from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from BD.models import User
from .forms import RegisterForm


# Create your views here.


@login_required
def profile_view(request):
    return render(request, 'avtorization/profile.html')


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            form.add_error('username', 'Пользователь с таким именем уже существует.')
            return self.form_invalid(form)
        form.save()
        return super().form_valid(form)