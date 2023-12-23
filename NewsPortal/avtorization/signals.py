from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import welcome_email_user

@receiver(post_save, sender=User)
def notify_new_post(sender, instance, created, **kwargs):
    if created:
        welcome_email_user.delay(instance.id)
