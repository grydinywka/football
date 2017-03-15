# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-15 20:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('football_app', '0012_auto_20170315_1931'),
    ]

    operations = [
        migrations.CreateModel(
            name='VotingList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_open', models.BooleanField(default=True)),
                ('list', jsonfield.fields.JSONField(blank=True)),
                ('tournament', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='football_app.Tournament')),
            ],
        ),
        migrations.AlterField(
            model_name='voting',
            name='list_voting',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='football_app.VotingList'),
        ),
        migrations.AlterUniqueTogether(
            name='voting',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='voting',
            name='final_place',
        ),
        migrations.RemoveField(
            model_name='voting',
            name='is_open',
        ),
        migrations.RemoveField(
            model_name='voting',
            name='tournament',
        ),
    ]