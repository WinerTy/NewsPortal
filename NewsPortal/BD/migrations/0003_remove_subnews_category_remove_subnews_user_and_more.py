# Generated by Django 5.0 on 2023-12-18 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BD', '0002_alter_subarticle_category_alter_subnews_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subnews',
            name='category',
        ),
        migrations.RemoveField(
            model_name='subnews',
            name='user',
        ),
        migrations.DeleteModel(
            name='SubArticle',
        ),
        migrations.DeleteModel(
            name='SubNews',
        ),
    ]
