# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-15 21:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('football_app', '0013_auto_20170315_2059'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='voting',
            unique_together=set([('contestant', 'list_voting')]),
        ),
    ]
