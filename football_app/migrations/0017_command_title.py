# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-16 18:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football_app', '0016_auto_20170315_2125'),
    ]

    operations = [
        migrations.AddField(
            model_name='command',
            name='title',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
