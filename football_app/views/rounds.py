from random import randint
import pandas as pd
import numpy as np

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
        if self.tournament.championship:
            games = Game.objects.filter(round=self.tournament.championship)
        else:
            games = None
        # print self.tournament.championship
        # print games
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
        messages.info(self.request, "Games were generated successfully")
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


class ChampionshipTable(DetailView):
    pk_url_kwarg = 'tid'
    template_name = 'football_app/championship_table.html'
    model = Tournament
    context_object_name = "tournament"

    def get_data_table(self):
        data_table = {}
        tournament = self.get_object()

        s = pd.Series([c for c in tournament.command_set.all()])
        # for command in tournament.command_set.all():
        #     dates = pd.date_range('20130101', periods=6)
        #     df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
        df = pd.DataFrame({'command' : s})
        df['played games'] = pd.Series([c.get_played_games_chip_count() for c in df['command'].values])
        df['wins'] = pd.Series([c.get_wins_chip() for c in df['command'].values])
        df['defeats'] = pd.Series([c.get_defeats_chip() for c in df['command'].values])
        df['equals'] = df['played games'].values - df['wins'].values - df['defeats'].values
        df['Goals - Goals Against'] = pd.Series(["{}-{}".format(c.goals_goals_against()[0],c.goals_goals_against()[1])
                                                 for c in df['command'].values])
        df['Difference'] = pd.Series([c.goals_goals_against()[0]-c.goals_goals_against()[1]
                                                 for c in df['command'].values])
        df['Points'] = df['wins'].values*3 + df['equals'].values

        df = df.sort_values(['Points'], axis=0,ascending=False)

        return df.to_html(
                            classes="table table-hover table-striped",
                            float_format=lambda x: '%.2f' % x,
                            index=False
                        )

    def get_context_data(self, **kwargs):
        context = super(ChampionshipTable, self).get_context_data(**kwargs)
        context['data_table'] = self.get_data_table()

        return context


class PlayoffGamesListView(ChampionshipGamesListView):
    template_name = "football_app/playoff_games_list.html"

    def get_queryset(self):
        # games = Game.objects.filter(round=self.tournament.playoff)
        if self.tournament.playoff:
            games = Game.objects.filter(round=self.tournament.playoff)
        else:
            games = None
        return games


class PlayoffGameCreateView(LoginRequiredMixinCustom, PermissionRequiredMixinCustom, CreateView):
    template_name = "football_app/playoff_game_create.html"
    model = Game
    fields = ('command1', 'command2', 'kind',)
    tournament = None

    def get_context_data(self, **kwargs):
        context = super(PlayoffGameCreateView, self).get_context_data(**kwargs)
        context['tournament'] = self.tournament

        return context

    def dispatch(self, request, *args, **kwargs):
        try:
            self.tournament = Tournament.objects.get(pk=self.kwargs['tid'])
        except Tournament.DoesNotExist:
            messages.warning(request, "Tournament with id == {} does not exist".format(self.kwargs['tid']))
            return HttpResponseRedirect(reverse('home'))

        return super(PlayoffGameCreateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.info(self.request, "Game was created successfully")
        return reverse('playoff_games_list', kwargs={'tid': self.kwargs['tid']})

    def get_free_commands(self):
        tournament_commands = Command.objects.filter(tournament__pk=self.kwargs['tid'])
        return tournament_commands

    def get_form(self, form_class=None):
        kwargs = self.get_form_kwargs()
        commands = self.get_free_commands()
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(**kwargs)
        choices = [(c.id, c) for c in commands]
        # choices.extend([(c.id, c) for c in self.get_object().get_contestants])
        form.fields['command1']._set_choices(choices)
        form.fields['command2']._set_choices(choices)
        # print dir(form.fields['kind'])
        form.fields['kind']._set_choices(form.fields['kind']._choices[1:])
        return form

    def post(self, request, *args, **kwargs):
        post_parent = super(PlayoffGameCreateView, self).post(request, *args, **kwargs)
        form = self.get_form()
        if request.POST.get('command1') == request.POST.get('command2'):
            # print dir(form)
            form.add_error("command1", "Check the command1")
            form.add_error("command2", "Check the command2")

            return self.form_invalid(form)

        return post_parent

    def form_valid(self, form):
        game = Game.objects.create(**form.cleaned_data)
        if self.tournament.playoff:
            self.tournament.playoff.games.add(game)
        else:
            playoff = Round.objects.create(description="playoff for Tournament #{}".format(self.tournament.id))
            self.tournament.playoff = playoff
            self.tournament.playoff.games.add(game)
            self.tournament.save()

        return HttpResponseRedirect(self.get_success_url())


class GameUpdateScore(LoginRequiredMixinCustom, PermissionRequiredMixinCustom, UpdateView):
    template_name = 'football_app/game_score_update.html'
    model = Game
    pk_url_kwarg = 'gid'
    tournament = None
    fields = ('score1', 'score2', 'status')

    def get_success_url(self):
        messages.info(self.request, "Score was updated for game {}".format(self.get_object()))
        if self.get_object().kind == CHAMPIONSHIP:
            return reverse('championship_games_list', kwargs={'tid': self.kwargs['tid']})
        return reverse('playoff_games_list', kwargs={'tid': self.kwargs['tid']})

    def get_context_data(self, **kwargs):
        context = super(GameUpdateScore, self).get_context_data(**kwargs)
        context['tournament'] = self.tournament

        return context

    def dispatch(self, request, *args, **kwargs):
        try:
            self.tournament = Tournament.objects.get(pk=self.kwargs['tid'])
        except Tournament.DoesNotExist:
            messages.warning(request, "Tournament with id == {} does not exist".format(self.kwargs['tid']))
            return HttpResponseRedirect(reverse('home'))

        return super(GameUpdateScore, self).dispatch(request, *args, **kwargs)


class PlayoffGameDeleteView(LoginRequiredMixinCustom, PermissionRequiredMixinCustom, DeleteView):
    template_name = 'football_app/playoff_game_delete.html'
    model = Game
    pk_url_kwarg = 'gid'

    def get_success_url(self):
        command = Game.objects.get(pk=self.kwargs['gid'])
        messages.success(self.request, 'Game {} successful deleted!'.format(command))
        return reverse('playoff_games_list', kwargs={'tid': self.kwargs['tid']})
