from django.conf.urls import url, include
from django.views.generic import TemplateView

from football_app.views.tournaments import TournamentView, CommandTitleUpdateView,\
    TournamentUpdateView, TournamentCreateView, FormCommandsView,\
    TourContestantsListView, TourCommandsListView, TourCommandUpdateView,\
    TourCommandCreateView, TourCommandDeleteView, PrevCommandsListView,\
    CurrentCommandsListView, PrevTournamentsListView, CurrentTournamentsListView

from football_app.views.rounds import ChampionshipGamesListView,\
    ChampionshipGamesGenerateView,PlayoffGamesListView,\
    PlayoffGameCreateView, GameUpdateScore,\
    PlayoffGameDeleteView, ChampionshipTable

from football_app.views.voting import VotingListCreateView, VotingBySortView,\
    VotingClose

urlpatterns = [
    url(r'^list/$', TournamentView.as_view(), name='home'),
    url(r'^(?P<tid>\d+)/command_title/(?P<cid>\d+)/update$', CommandTitleUpdateView.as_view(),
        name="command_title_update"),
    url(r'^create/$', TournamentCreateView.as_view(), name="tournament_create"),
    url(r'^form_command/$', FormCommandsView.as_view(), name="form_commands"),
    url(r'^(?P<tid>\d+)/contestants_list/$', TourContestantsListView.as_view(), name="tournament_contestants_list"),
    url(r'^(?P<tid>\d+)/update/$', TournamentUpdateView.as_view(),
        name="tournament_update"),
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
    url(r'^(?P<tid>\d+)/voting/$', VotingBySortView.as_view(),
        name="voting"),
    url(r'^voting/create$', VotingListCreateView.as_view(),
        name="voting_create"),
    url(r'^voting/closing$', VotingClose.as_view(),
        name="voting_closing"),

    url(r'^(?P<uid>\d+)/prev_commands$', PrevCommandsListView.as_view(),
        name="prev_commands"),
    url(r'^(?P<uid>\d+)/current_commands$', CurrentCommandsListView.as_view(),
        name="current_commands"),
    url(r'^(?P<uid>\d+)/prev_tournaments$', PrevTournamentsListView.as_view(),
        name="prev_tournaments"),
    url(r'^(?P<uid>\d+)/curr_tournaments$', CurrentTournamentsListView.as_view(),
        name="curr_tournaments"),

]
