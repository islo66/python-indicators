# Generated by Django 2.2.1 on 2019-05-20 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IE', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='regions',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='regions',
            name='date_updated',
        ),
    ]
