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
from football_app.models import Tournament, Command, Round, Game
from football_app.forms import ChampionshipGamesGenerateForm


class ChampionshipGamesListView(LoginRequiredMixinCustom, ListView):
    template_name = "football_app/championship_games_list.html"
    model = Round
    context_object_name = 'rounds'
    tournament = None

    def get_context_data(self, **kwargs):
        context = super(ChampionshipGamesListView, self).get_context_data(**kwargs)
        context['tournament'] = self.tournament

        return context

    def get_queryset(self):
        rounds = Round.objects.filter(tournament=self.tournament)
        return rounds

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

    def generate_rounds(self, amount_games):
        pass

    def form_valid(self, form):
        amount = form.cleaned_data['amount']
        print amount
        return HttpResponseRedirect(self.get_success_url())