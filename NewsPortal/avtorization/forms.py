from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import Group
from captcha.fields import CaptchaField
from .tasks import welcome_email_user
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    captcha = CaptchaField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'captcha')


    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            basic_group = Group.objects.get(name='common')
            basic_group.user_set.add(user)
            welcome_email_user.delay(user.id)
        return user