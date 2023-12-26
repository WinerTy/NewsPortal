from django.core.management.base import BaseCommand, CommandError
from BD.models import Post

class Command(BaseCommand):
    help = 'Подсказка вашей команды'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True  # напоминать ли о миграциях. Если true — то будет напоминание о том, что не сделаны все миграции (если такие есть)


    def handle(self, *args, **options):
        self.stdout.write('Какой тип публикации вы хотите удалить? news/article')
        types = input()

        if types == 'news':
            self.stdout.write(f'Вы действительно хотите удалить все публикации которые относятся к {types}. yes/no')
            answer = input()
            if answer == 'yes':
                Post.objects.filter(type='news').delete()
                self.stdout.write('Все публикации типа News были удалены!')
                return
            if answer == 'no':
                self.stdout.write(self.style.ERROR('Вы отменили даннеое действие'))
        if types == 'article':
            self.stdout.write(f'Вы действительно хотите удалить все публикации которые относятся к {types}. yes/no')
            answer = input()
            if answer == 'yes':
                Post.objects.filter(type='article').delete()
                self.stdout.write('Все публикации типа Article были удалены!')
                return
            if answer == 'no':
                self.stdout.write(self.style.ERROR('Вы отменили даннеое действие'))

        self.stdout.write(self.style.ERROR('Отмена'))