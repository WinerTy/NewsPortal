from NewsPortal.settings import DEFAULT_FROM_EMAIL
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import Group
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import redirect
from django.template.loader import render_to_string


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            basic_group = Group.objects.get(name='common')
            basic_group.user_set.add(user)

            html_content = render_to_string(
                'MailPost/Email.html', {'user': user}
            )

            msg = EmailMultiAlternatives(
                f'{user}, Спасибо за регистрацию',  # subject
                '',
                f'{DEFAULT_FROM_EMAIL}',  # from email
                [f'{user.email}'],  # recipient list
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html
            msg.send()
            print('Письмо отправлено')

        return user