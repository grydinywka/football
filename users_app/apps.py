from __future__ import unicode_literals

from django.apps import AppConfig


class UsersAppConfig(AppConfig):
    name = 'users_app'

    def ready(self):
        from users_app import signals
