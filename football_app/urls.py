from django.conf.urls import url, include
from django.views.generic import TemplateView

from football_app.views.tournaments import TournamentView, TournamentDetailView,\
    TournContestantsUpdateView, TournamentCreateView, FormCommandsView,\
    TourContestantsListView, TourCommandsListView, TourCommandUpdateView,\
    TourCommandCreateView, TourCommandDeleteView

from football_app.views.rounds import ChampionshipGamesListView,\
    ChampionshipGamesGenerateView,PlayoffGamesListView,\
    PlayoffGameCreateView, GameUpdateScore,\
    PlayoffGameDeleteView, ChampionshipTable

from football_app.views.voting import VotingListCreateView

urlpatterns = [
    url(r'^list/$', TournamentView.as_view(), name='home'),
    url(r'^(?P<tid>\d+)/detail/$', TournamentDetailView.as_view(), name="tournament_detail"),
    url(r'^create/$', TournamentCreateView.as_view(), name="tournament_create"),
    url(r'^form_command/$', FormCommandsView.as_view(), name="form_commands"),
    url(r'^(?P<tid>\d+)/contestants_list/$', TourContestantsListView.as_view(), name="tournament_contestants_list"),
    url(r'^(?P<tid>\d+)/contestants_update/$', TournContestantsUpdateView.as_view(),
        name="tournament_contestants_update"),
    url(r'^(?P<tid>\d+)/commands_list/$', TourCommandsListView.as_view(), name="tournament_commands_list"),
    url(r'^(?P<tid>\d+)/command_create/$', TourCommandCreateView.as_view(),
        name="tournament_command_create"),
    url(r'^(?P<tid>\d+)/command_update/(?P<comid>\d+)$', TourCommandUpdateView.as_view(),
        name="tournament_command_update"),
    url(r'^(?P<tid>\d+)/command_delete/(?P<comid>\d+)$', TourCommandDeleteView.as_view(),
        name="tournament_command_delete"),

    # rounds section
    url(r'^(?P<tid>\d+)/championship/$', ChampionshipGamesListView.as_view(),
        name="championship_games_list"),
    url(r'^(?P<tid>\d+)/championship/games/generate/$', ChampionshipGamesGenerateView.as_view(),
        name="championship_games_generate"),
    url(r'^(?P<tid>\d+)/championship/table/$', ChampionshipTable.as_view(),
        name="championship_table"),
    url(r'^(?P<tid>\d+)/playoff/$', PlayoffGamesListView.as_view(),
        name="playoff_games_list"),
    url(r'^(?P<tid>\d+)/playoff/game/create/$', PlayoffGameCreateView.as_view(),
        name="playoff_game_create"),
    url(r'^(?P<tid>\d+)/game/(?P<gid>\d+)/score_update/$', GameUpdateScore.as_view(),
        name="game_score_update"),
    url(r'^(?P<tid>\d+)/playoff/game/(?P<gid>\d+)/delete/$', PlayoffGameDeleteView.as_view(),
        name="playoff_game_delete"),

    # voting
    url(r'^(?P<tid>\d+)/voting/$', TemplateView.as_view(template_name="football_app/voting/voting_by_sort.html"),
        name="voting"),
    url(r'^voting/create$', VotingListCreateView.as_view(
        template_name="football_app/voting/voting_create.html"),
        name="voting_create"),
]
