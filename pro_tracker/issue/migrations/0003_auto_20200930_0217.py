# Generated by Django 3.1.1 on 2020-09-29 19:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('issue', '0002_auto_20200929_0329'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='author',
        ),
        migrations.AddField(
            model_name='issue',
            name='author',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
