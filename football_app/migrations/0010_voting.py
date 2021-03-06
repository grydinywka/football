# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-15 18:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('football_app', '0009_auto_20170315_0904'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_voted', models.BooleanField(default=False)),
                ('is_open', models.BooleanField(default=True)),
                ('final_place', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('list_voting', jsonfield.fields.JSONField()),
                ('contestant', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tournament', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='football_app.Tournament')),
            ],
        ),
    ]
