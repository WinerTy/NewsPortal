from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Welcome to',
            'ТЕКСТ_ЗАГЛУШКА',
            'NewsPortal.com',
            [instance.email],
            fail_silently=True,
        )