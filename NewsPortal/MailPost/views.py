from NewsPortal.settings import DEFAULT_FROM_EMAIL

from django.contrib.auth.models import Group, User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.shortcuts import redirect

from BD.models import Post

from django.template.loader import render_to_string
from django.urls import reverse



@receiver(post_save, sender=Post)
def notify_new_post(sender, instance, created, **kwargs):
    groups = Group.objects.filter(name__in=['article', 'news'])
    for group in groups:
        users = group.user_set.all()  # Получаем всех пользователей в группе
        for user in users:
            if group.name == 'article':
                type = 'Статья'
            elif group.name == 'news':
                type = 'Новость'

            subject = {
                'title': f'{instance.title}',
                'author': f'{instance.author}',
                'type': f'{type}',
                'data': f'{instance.date}',
                'text': f'{instance.text}',
                'url': reverse('Post Details', args=[instance.id]),
            }

            html_content = render_to_string(
                'MailPost/NewPostEmail.html', {
                    'subject': subject,
                }
            )

            msg = EmailMultiAlternatives(
                'На портале NewsPortal, вышел новый пост!',
                '',
                f'{DEFAULT_FROM_EMAIL}',
                [user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

class Subscriber():     # pylint: disable=                                      # ПЕРЕДЕЛАТЬ
    def get_role_news(request):
        if request.user.is_authenticated:
            group = Group.objects.get(name='news')
            request.user.groups.add(group)
        return redirect('/main')

    def get_role_article(request):
        if request.user.is_authenticated:
            group = Group.objects.get(name='article')
            request.user.groups.add(group)
        return redirect('/main')

    def remove_role_news(request):
        if request.user.is_authenticated:
            group = Group.objects.get(name='news')
            request.user.groups.remove(group)
        return redirect('/main')

    def remove_role_article(request):
        if request.user.is_authenticated:
            group = Group.objects.get(name='article')
            request.user.groups.remove(group)
        return redirect('/main')

    def remove_role_sub(request):
        if request.user.is_authenticated:
            groups = Group.objects.filter(name__in=['article', 'news'])
            for group in groups:
                request.user.groups.remove(group)
        return redirect('/main')