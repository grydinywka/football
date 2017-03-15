from __future__ import unicode_literals

from django.apps import AppConfig


class FootballAppConfig(AppConfig):
    name = 'football_app'

    def ready(self):
        from football_app import signals
