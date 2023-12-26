from __future__ import absolute_import, unicode_literals

from datetime import timedelta

from celery import shared_task


from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse

from NewsPortal.settings import DEFAULT_FROM_EMAIL

from BD.models import Post, PostCategory
from django.utils import timezone



@shared_task
def notify_new_post_task(post_id):
    post = Post.objects.get(id=post_id)
    category = ', '.join(str(e) for e in PostCategory.objects.filter(post__id=post_id).values_list('category__name', flat=True))
    print(category)
    groups = Group.objects.filter(name__in=['article', 'news'])
    for group in groups:
        users = group.user_set.all()  # Получаем всех пользователей в группе
        for user in users:
            if group.name == 'article':
                type = 'Статья'
            elif group.name == 'news':
                type = 'Новость'

            subject = {
                'title': f'{post.title}',
                'author': f'{post.author}',
                'type': f'{type}',
                'data': f'{post.date}',
                'text': f'{post.text}',
                'category': f'{category}',
                'url': reverse('Post Details', args=[post.id]),
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

@shared_task
def week_results():
    groups = Group.objects.filter(name__in=['article', 'news'])
    for group in groups:
        users = group.user_set.all()
        post_type = 'news' if group.name == 'news' else 'article'
        posts = Post.objects.filter(created_at__gte=timezone.now() - timedelta(days=7), type=post_type)

        if posts.exists():
            # Формируем сообщение
            post_list = []
            for post in posts:
                if post.type == 'news':
                    type = 'Новость'
                else:
                    type = 'Статья'

                post_list.append({
                    'title': post.title,
                    'author': post.author,
                    'type': type,
                    'date': post.date,
                    'text': post.text,
                    'url': reverse('Post Details', args=[post.id]),
                })

            html_content = render_to_string(
                'MailPost/NewsEmailweek.html', {
                    'post_list': post_list,
                }
            )

            for user in users:
                msg = EmailMultiAlternatives(
                    'Итоги недели на портале NewsPortal',
                    '',
                    f'{DEFAULT_FROM_EMAIL}',
                    [user.email]
                )

                msg.attach_alternative(html_content, "text/html")
                msg.send()