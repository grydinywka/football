from django.conf.urls import url, include

from football_app.views import TournamentView, TournamentDetailView,\
    TournamentUsersUpdateView, TournamentCreateView, FormTeamsView,\
    TourUsersListView, TourCommandsListView, TourCommandUpdateView,\
    TourCommandCreateView, TourCommandDeleteView

urlpatterns = [
    url(r'^(?P<tid>\d+)/detail/$', TournamentDetailView.as_view(), name="tournament_detail"),
    url(r'^(?P<tid>\d+)/users_update/$', TournamentUsersUpdateView.as_view(), name="tournament_users_update"),
    url(r'^create/$', TournamentCreateView.as_view(), name="tournament_create"),
    url(r'^form_team/$', FormTeamsView.as_view(), name="form_teams"),
    url(r'^(?P<tid>\d+)/users_list/$', TourUsersListView.as_view(), name="tournament_users_list"),
    url(r'^(?P<tid>\d+)/commands_list/$', TourCommandsListView.as_view(), name="tournament_commands_list"),
    url(r'^(?P<tid>\d+)/command_create/$', TourCommandCreateView.as_view(),
        name="tournament_command_create"),
    url(r'^(?P<comid>\d+)/command_update/$', TourCommandUpdateView.as_view(),
        name="tournament_command_update"),
    url(r'^(?P<comid>\d+)/command_delete/$', TourCommandDeleteView.as_view(),
        name="tournament_command_delete"),
]
