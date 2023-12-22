from django.db.models.signals import post_save
from django.dispatch import receiver

from BD.models import Post
from .tasks import notify_new_post_task

@receiver(post_save, sender=Post)
def notify_new_post(sender, instance, created, **kwargs):
    if created:
        notify_new_post_task.delay(instance.id)
