from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView,\
                                 UpdateView, CreateView, FormView,\
                                 RedirectView, DeleteView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from users_app.views import LoginRequiredMixinCustom, PermissionRequiredMixinCustom
from football_app.models import Tournament, Command, Round, Game,\
    IS_NOT_STARTED, CURRENT, ENDED,\
    CHAMPIONSHIP, PLAYOFF_1_16, PLAYOFF_1_8, PLAYOFF_1_4,\
    PLAYOFF_1_2, PLAYOFF_1_1, PLAYOFF_3, Voting, VotingList
from football_app.forms import ChampionshipGamesGenerateForm


class VotingCreateView(LoginRequiredMixinCustom, PermissionRequiredMixinCustom, CreateView):
    template_name = "football_app/voting/voting_create.html"
    model = VotingList
    fields = ('tournament',)

    def get_success_url(self):
        messages.info(self.request, "VotingList for tournament #{} was created".format(self.get_object().tournament.id))
        return reverse("cabinet")

    def is_valid(self, form):
        tournament = form.cleaned_data['tournament']
        voting_list = VotingList.objects.create(tournament=tournament)
