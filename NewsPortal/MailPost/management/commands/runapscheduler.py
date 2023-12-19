from datetime import timedelta
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.contrib.auth.models import Group, User
from django.core.mail import EmailMultiAlternatives, send_mail
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.urls import reverse
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from NewsPortal.settings import DEFAULT_FROM_EMAIL

from BD.models import Post

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран

def my_job():
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
                print("Письма успешно отправлены:")
                print(f'{user} - {user.email}')

# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day="*/7"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")