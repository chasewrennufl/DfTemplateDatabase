# Generated by Django 4.0.4 on 2022-07-18 20:48

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('survey', '0015_intent'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Intent',
            new_name='IntentList',
        ),
    ]
