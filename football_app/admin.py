from django.contrib import admin

from football_app.models import Tournament, Command, Round, Game


class CommandAdmin(admin.ModelAdmin):
    list_display = ['id', 'tournament', 'contestant1', 'contestant2']

admin.site.register(Tournament)
admin.site.register(Command, CommandAdmin)
admin.site.register(Round)
admin.site.register(Game)