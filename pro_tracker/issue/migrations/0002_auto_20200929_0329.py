# Generated by Django 3.1.1 on 2020-09-28 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='priority',
            field=models.CharField(choices=[('high', 'high'), ('medium', 'medium'), ('low', 'low')], max_length=30),
        ),
    ]
