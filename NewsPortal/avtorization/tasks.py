from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from NewsPortal.settings import DEFAULT_FROM_EMAIL


@shared_task
def welcome_email_user(id):
    user = User.objects.get(id=id)
    data = {
        'username': user.username,
        'email': user.email
    }
    html_content = render_to_string(
        'MailPost/Email.html', {'user': data}
    )

    msg = EmailMultiAlternatives(
        f'{user.username}, Спасибо за регистрацию!',
        '',
        f'{DEFAULT_FROM_EMAIL}',
        [f'{user.email}'],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()