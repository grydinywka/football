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


class VotingListCreateView(LoginRequiredMixinCustom, PermissionRequiredMixinCustom, CreateView):
    template_name = "football_app/voting/voting_create.html"
    model = VotingList
    fields = ('tournament',)

    def get_success_url(self):
        messages.info(self.request, "VotingList was created")
        return reverse("cabinet")

    def get_initial(self):
        initials = self.initial.copy()
        print initials
        return self.initial.copy()

    def get_form(self, form_class=None):
        kwargs = self.get_form_kwargs()
        tournaments = Tournament.objects.filter(status=ENDED)
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(**kwargs)
        choices = [(t.id, t) for t in tournaments]
        form.fields['tournament']._set_choices(choices)
        return form