from random import randint

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
    IS_NOT_STARTED, ENDED,\
    CHAMPIONSHIP, PLAYOFF_1_16, PLAYOFF_1_8, PLAYOFF_1_4,\
    PLAYOFF_1_2, PLAYOFF_1_1, PLAYOFF_3
from football_app.forms import ChampionshipGamesGenerateForm


class ChampionshipGamesListView(LoginRequiredMixinCustom, ListView):
    template_name = "football_app/championship_games_list.html"
    model = Game
    context_object_name = 'games'
    tournament = None

    def get_context_data(self, **kwargs):
        context = super(ChampionshipGamesListView, self).get_context_data(**kwargs)
        context['tournament'] = self.tournament

        return context

    def get_queryset(self):
        games = Game.objects.filter(round=self.tournament.championship)
        return games

    def dispatch(self, request, *args, **kwargs):
        try:
            self.tournament = Tournament.objects.get(pk=self.kwargs['tid'])
        except Tournament.DoesNotExist:
            messages.warning(request, "Tournament with id == {} does not exist".format(self.kwargs['tid']))
            return HttpResponseRedirect(reverse('home'))

        return super(ChampionshipGamesListView, self).dispatch(request, *args, **kwargs)


class ChampionshipGamesGenerateView(LoginRequiredMixinCustom, PermissionRequiredMixinCustom, FormView):
    template_name = 'football_app/championship_games_generate.html'
    form_class = ChampionshipGamesGenerateForm
    tournament = None

    def get_success_url(self):
        return reverse('championship_games_list', kwargs={'tid': self.kwargs['tid']})

    def dispatch(self, request, *args, **kwargs):
        try:
            self.tournament = Tournament.objects.get(pk=self.kwargs['tid'])
        except Tournament.DoesNotExist:
            messages.warning(request, "Tournament with id == {} does not exist".format(self.kwargs['tid']))
            return HttpResponseRedirect(reverse('home'))

        return super(ChampionshipGamesGenerateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ChampionshipGamesGenerateView, self).get_context_data(**kwargs)
        context['tournament'] = self.tournament

        return context

    def generate_games(self, amount_games):

        try:
            championship = Round.objects.get(tournament_chip=self.tournament)
        except Round.DoesNotExist:
            championship = Round.objects.create(
                    description="championchip for {}".format(self.tournament))
            self.tournament.championship = championship
            self.tournament.save()
        else:
            championship.games.all().delete()
        commands = self.tournament.command_set.all()
        # print championship
        for i in xrange(0,commands.count()-1):
            j = i + 1
            while j < commands.count():
                for k in range(amount_games):
                    game = Game.objects.create(
                        command1=commands[i],
                        command2=commands[j],
                        status=IS_NOT_STARTED,
                        kind=CHAMPIONSHIP
                    )
                    championship.games.add(game)
                j += 1

    def form_valid(self, form):
        amount = form.cleaned_data['amount']
        # print amount
        self.generate_games(amount)
        return HttpResponseRedirect(self.get_success_url())