from random import randint

from django.shortcuts import render
from django.db.models import Q
from django.views.generic import TemplateView, ListView, DetailView,\
                                 UpdateView, CreateView, FormView,\
                                 RedirectView, DeleteView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from users_app.views import LoginRequiredMixinCustom, PermissionRequiredMixinCustom
from football_app.models import Tournament, Command, Round, Game,\
    IS_NOT_STARTED, CURRENT, ENDED
from football_app.forms import CreateToutnamentForm, UpdateTourForm,\
                               CreateTournCommandForm


class TournamentView(LoginRequiredMixinCustom, ListView):
    template_name='football_app/tournaments_list.html'
    context_object_name = 'tournaments'
    model = Tournament


class TournamentCreateView(LoginRequiredMixinCustom, PermissionRequiredMixinCustom,
                           CreateView):
    template_name = 'football_app/tournament_create.html'
    model = Tournament
    fields = ('title', 'contestants',)

    def get_success_url(self):
        obj = self.object
        return reverse('tournament_contestants_list', kwargs={'tid': obj.id})

# class TournamentCreateView(FormView):
#     template_name = 'football_app/tournament_create.html'
#     # model = Tournament
#     form_class = CreateToutnamentForm
#     # fields = ('rounds', 'commands', 'status')
#     success_url = '/users/cabinet/'
#
#     def post(self, request, *args, **kwargs):
#         form = self.get_form()
#         if form.is_valid():
#             users = form.cleaned_data['users']
#             print users
#         return HttpResponseRedirect(reverse('home'))


class FormCommandsView(LoginRequiredMixinCustom, PermissionRequiredMixinCustom,
                       RedirectView):
    """Automatically forms command - command must be pair
       After that - redirect"""

    def form_commands(self, tournament, request, tourn_id):
        for command in tournament.command_set.all():
            command.delete()

        contestants = tournament.contestants.all().order_by('rateuser__rate', 'id')
        limit = contestants.count()
        if limit == 0:
            messages.warning(request, "No contestants :(")
        elif limit % 2 != 0:
            messages.warning(request, "There are {} contestant, but for forming teams\
                                        should be pair.".format(contestants.count()))
        else:
            i, j = 0, limit-1
            while i < j-1:
                rand = randint(0,1)
                if rand == 0:
                    Command.objects.create(tournament=tournament,
                                       contestant1=contestants[i],
                                       contestant2=contestants[j])
                    Command.objects.create(tournament=tournament,
                                       contestant1=contestants[i+1],
                                       contestant2=contestants[j-1])
                else:
                    Command.objects.create(tournament=tournament,
                                       contestant1=contestants[i+1],
                                       contestant2=contestants[j])
                    Command.objects.create(tournament=tournament,
                                       contestant1=contestants[i],
                                       contestant2=contestants[j-1])
                i += 2
                j -= 2

            if i < j:
                Command.objects.create(tournament=tournament,
                                       contestant1=contestants[i],
                                       contestant2=contestants[j])

            messages.info(request, "Commands for tournament #{} were formed!".format(tourn_id))

    def get(self, request,  *args, **kwargs):
        tourn_id = request.GET.get('tournament')
        if tourn_id:
            tournament = Tournament.objects.get(pk=tourn_id)
            self.url = reverse('tournament_commands_list', kwargs={'tid':tourn_id})
            self.form_commands(tournament, request, tourn_id)
        else:
            self.url = reverse('home')
        return super(FormCommandsView, self).get(request,  *args, **kwargs)


class TourContestantsListView(DetailView):
    """
        returns List of contestants of certain tournaments
    """
    template_name = 'football_app/tournament_contestants_list.html'
    model = Tournament
    pk_url_kwarg = 'tid'


class TourCommandsListView(DetailView):
    """
        returns List of commands of certain tournaments
        If it is specified filter `player` we are filtering commands by contestants
    """
    template_name = 'football_app/tournament_commands_list.html'
    pk_url_kwarg = 'tid'
    model = Tournament

    def get_context_data(self, **kwargs):
        context = super(TourCommandsListView, self).get_context_data(**kwargs)
        player = self.request.GET.get("player")
        commands = self.get_object().command_set.all()
        if player:
            commands = commands.filter(
                                 Q(contestant1__first_name__icontains=player) |
                                 Q(contestant2__first_name__icontains=player) |
                                 Q(contestant1__last_name__icontains=player) |
                                 Q(contestant2__last_name__icontains=player)
                                 )
        context['commands'] = commands
        return context


class TournamentUpdateView(LoginRequiredMixinCustom, PermissionRequiredMixinCustom,
                           UpdateView):
    """
        The View for update tournament: list of contestants ans status
    """
    template_name = 'football_app/tournament_update.html'
    pk_url_kwarg = 'tid'
    model = Tournament
    form_class = UpdateTourForm

    # fields = ('users',)

    def get_form(self, form_class=None):
        kwargs = self.get_form_kwargs()
        kwargs['initial']['users_pk'] = [u.pk for u in self.object.contestants.all()]
        # print kwargs
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**kwargs)

    def get_success_url(self):
        obj = self.object
        return reverse('tournament_contestants_list', kwargs={'tid': obj.id})


class TourCommandCreateView(LoginRequiredMixinCustom, PermissionRequiredMixinCustom,
                            CreateView):
    """
        The view for manual creating commands for certain tournament
    """
    template_name = 'football_app/tournament_command_create.html'
    pk_url_kwarg = 'tid'
    model = Command
    # fields = ('contestant1', 'contestant2',)
    form_class = CreateTournCommandForm

    def get_success_url(self):
        return reverse('tournament_commands_list', kwargs={"tid": self.kwargs['tid']})

    def get(self, request,  *args, **kwargs):
        if 'tid' in self.kwargs:
            return super(TourCommandCreateView, self).get(request,  *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))

    def get_context_data(self, **kwargs):
        context = super(TourCommandCreateView, self).get_context_data(**kwargs)
        context['tournament'] = Tournament.objects.get(pk=self.kwargs['tid'])
        if self.get_free_contestant():
            context['are_contestants'] = True
        else:
            context['are_contestants'] = False

        return context

    def form_valid(self, form):
        tournament = Tournament.objects.get(pk=self.kwargs['tid'])
        command = Command.objects.create(tournament=tournament,
            contestant1=form.cleaned_data['contestant1'],
            contestant2=form.cleaned_data['contestant2']
            )
        messages.success(self.request, 'Command {} successful created!'.format(command))

        return HttpResponseRedirect(self.get_success_url())

    def get_free_contestant(self):
        tournament_commands = Command.objects.filter(tournament__pk=self.kwargs['tid'])
        contestants = User.objects.filter(tournament__id=self.kwargs['tid'])\
            .exclude(contestant1__in=tournament_commands)\
            .exclude(command__in=tournament_commands)
        return contestants

    def get_form(self, form_class=None):
        kwargs = self.get_form_kwargs()
        contestants = self.get_free_contestant()
        kwargs['initial']['contestants'] = [c for c in contestants]
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**kwargs)


class TourCommandUpdateView(LoginRequiredMixinCustom, PermissionRequiredMixinCustom,
                            UpdateView):
    """
        The view for updating specified command - its contestants
    """
    template_name = 'football_app/tournament_command_update.html'
    pk_url_kwarg = 'comid'
    model = Command
    fields = ('contestant1', 'contestant2',)

    def get_tournament_id(self):
        return self.kwargs['tid']

    def get_success_url(self):
        messages.success(self.request, 'Command {} successful updated!'.format(self.get_object()))
        return reverse('tournament_commands_list', kwargs={"tid": self.get_tournament_id()})

    def get_free_contestant(self):
        tournament_commands = Command.objects.filter(tournament__pk=self.get_tournament_id())
        contestants = User.objects.filter(tournament__id=self.get_tournament_id())\
            .exclude(contestant1__in=tournament_commands)\
            .exclude(command__in=tournament_commands)
        return contestants

    def get_form(self, form_class=None):
        kwargs = self.get_form_kwargs()
        contestants = self.get_free_contestant()
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(**kwargs)
        choices = [(c.id, c) for c in contestants]
        choices.extend([(c.id, c) for c in self.get_object().get_contestants])
        form.fields['contestant1']._set_choices(choices)
        form.fields['contestant2']._set_choices(choices)
        return form

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if request.POST.get('contestant1') == request.POST.get('contestant2'):
            # print dir(form)
            form.add_error("contestant1", "Check the contestant1")
            form.add_error("contestant2", "Check the contestant2")

            return self.form_invalid(form)

        return super(TourCommandUpdateView, self).post(request, *args, **kwargs)


class TourCommandDeleteView(LoginRequiredMixinCustom, PermissionRequiredMixinCustom,
                            DeleteView):
    """
        The view for destroying command
    """
    template_name = 'football_app/tournament_command_delete.html'
    model = Command
    pk_url_kwarg = 'comid'

    def get_success_url(self):
        command = Command.objects.get(pk=self.kwargs['comid'])
        messages.success(self.request, 'Command {} successful deleted!'.format(command))
        return reverse('tournament_commands_list', kwargs={'tid': command.tournament.id})


class PrevCommandsListView(LoginRequiredMixinCustom, ListView):
    """
        The view for getting list of previous commands of the contestant. Tournament status is ENDED
    """

    template_name='football_app/prev_curr_command.html'
    context_object_name = 'commands'
    model = Command

    def get_commands(self):
        commands = Command.objects.filter(
            Q(contestant1__pk=self.kwargs['uid']) |
            Q(contestant2__pk=self.kwargs['uid'])
        )
        return commands

    def get_queryset(self):
        commands = self.get_commands()
        return commands.filter(tournament__status=ENDED)

    def get_context_data(self, **kwargs):
        context = super(PrevCommandsListView, self).get_context_data(**kwargs)
        context['which'] = 'previous'

        return context


class CurrentCommandsListView(PrevCommandsListView):
    """
        The view for getting list of current commands of the contestant. Tournament status is CURRENT
    """
    def get_queryset(self):
        commands = self.get_commands()
        return commands.filter(tournament__status=CURRENT)

    def get_context_data(self, **kwargs):
        context = super(CurrentCommandsListView, self).get_context_data(**kwargs)
        context['which'] = 'current'

        return context


class PrevTournamentsListView(LoginRequiredMixinCustom, ListView):
    """
        The view for getting list of previous tournaments of the contestant. Tournament status is ENDED
    """
    template_name='football_app/prev_curr_tournament.html'
    context_object_name = 'tournaments'
    model = Tournament

    def get_tournaments(self):
        tournaments = Tournament.objects.filter(contestants__pk=self.kwargs['uid'])
        return tournaments

    def get_queryset(self):
        tournaments = self.get_tournaments()
        return tournaments.filter(status=ENDED)

    def get_context_data(self, **kwargs):
        context = super(PrevTournamentsListView, self).get_context_data(**kwargs)
        context['which'] = 'previous'

        return context


class CurrentTournamentsListView(PrevTournamentsListView):
    """
        The view for getting list of current tournaments of the contestant. Tournament status is CURRENT
    """
    def get_queryset(self):
        tournaments = self.get_tournaments()
        return tournaments.filter(status=CURRENT)

    def get_context_data(self, **kwargs):
        context = super(CurrentTournamentsListView, self).get_context_data(**kwargs)
        context['which'] = 'current'

        return context


class CommandTitleUpdateView(LoginRequiredMixinCustom, UpdateView):
    """
        The view for updating title(name) of current command of contestant
    """
    pk_url_kwarg = 'cid'
    template_name = 'football_app/command_title_update.html'
    model = Command
    fields = ('title',)

    def get_success_url(self):
        messages.info(self.request, "Title od command #{} changed!".format(self.get_object().id))
        return reverse('current_commands', kwargs={'uid': self.request.user.id})

    def get(self, request, *args, **kwargs):
        command = self.get_object()
        if request.user not in command.get_contestants:
            messages.info(self.request, "You do not allow change command #{}!".format(self.get_object().id))
            return HttpResponseRedirect(reverse('cabinet'))
        if command.tournament.status != CURRENT:
            messages.info(self.request, "You  allow change command only for current commands!")
            return HttpResponseRedirect(reverse('cabinet'))

        return super(CommandTitleUpdateView, self).get(request, *args, **kwargs)