# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-15 21:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('football_app', '0015_auto_20170315_2107'),
    ]

    operations = [
        migrations.RenameField(
            model_name='voting',
            old_name='list_voting',
            new_name='voting_list',
        ),
        migrations.AlterUniqueTogether(
            name='voting',
            unique_together=set([('contestant', 'voting_list')]),
        ),
    ]
