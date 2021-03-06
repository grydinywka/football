# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-14 17:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football_app', '0005_auto_20170314_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='championship',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='championship', to='football_app.Round'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='playoff',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='football_app.Round'),
        ),
    ]
