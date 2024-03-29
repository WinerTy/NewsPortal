from django.db import models
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group



class BaseSignForm(SignupForm):

    def save(self, request):
        user = super(BaseSignForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user