from django.contrib import admin

from football_app.models import Tournament, Command, Round, Game, Voting, VotingList


class CommandAdmin(admin.ModelAdmin):
    list_display = ['id', 'tournament', 'contestant1', 'contestant2']


class VotingAdmin(admin.ModelAdmin):
    list_display = ['id', 'contestant', 'is_voted', 'voting_list']

class VotingListAdmin(admin.ModelAdmin):
    list_display = ['id', 'tournament', 'is_open', 'list']

admin.site.register(Tournament)
admin.site.register(Command, CommandAdmin)
admin.site.register(Round)
admin.site.register(Game)
admin.site.register(Voting, VotingAdmin)
admin.site.register(VotingList, VotingListAdmin)