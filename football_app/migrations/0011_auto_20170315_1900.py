# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-15 19:00
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('football_app', '0010_voting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voting',
            name='list_voting',
            field=jsonfield.fields.JSONField(blank=True),
        ),
    ]
