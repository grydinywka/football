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
from football_app.forms import CreateToutnamentForm, UpdateTourUsersForm,\
                               CreateTournCommandForm


class TournamentView(LoginRequiredMixinCustom, ListView):
    template_name='football_app/tournaments_list.html'
    context_object_name = 'tournaments'
    model = Tournament


class TournamentDetailView(DetailView):
    pk_url_kwarg = 'tid'
    template_name = 'football_app/tournament_detail.html'
    model = Tournament
    # context_object_name = 'tournament'

    # def get_context_data(self, **kwargs):
    #     context = super(TournamentDetailView, self).get_context_data(**kwargs)
    #     context['users'] = User.objects.all()
    #
    #     return context


class TournamentCreateView(LoginRequiredMixinCustom, PermissionRequiredMixinCustom, CreateView):
    template_name = 'football_app/tournament_create.html'
    model = Tournament
    fields = ('title', 'users',)

    def get_success_url(self):
        obj = self.object
        return reverse('tournament_update', kwargs={'tid': obj.id})

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

# def create(request):
#     form = CreateToutnamentForm()
#     return render(request, 'football_app/tournament_create.html', {'form': form})


class FormCommandsView(LoginRequiredMixinCustom, PermissionRequiredMixinCustom, RedirectView):
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


class TourUsersListView(DetailView):
    template_name = 'football_app/tournament_users_list.html'
    model = Tournament
    pk_url_kwarg = 'tid'


class TourCommandsListView(DetailView):
    template_name = 'football_app/tournament_commands_list.html'
    pk_url_kwarg = 'tid'
    model = Tournament


class TournamentUsersUpdateView(LoginRequiredMixinCustom, PermissionRequiredMixinCustom, UpdateView):
    template_name = 'football_app/tournament_users_update.html'
    pk_url_kwarg = 'tid'
    model = Tournament
    form_class = UpdateTourUsersForm

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
        return reverse('tournament_users_list', kwargs={'tid': obj.id})


# class TourCommandUpdateView(UpdateView):
#     template_name = 'football_app/tournament_command_update.html'
#     pk_url_kwarg = 'tid'
#     model = Tournament
#     form_class = UpdateTourCommandForm
#
#     def get_form(self, form_class=None):
#         kwargs = self.get_form_kwargs()
#         kwargs['initial']['commands_pk'] = [c.pk for c in self.get_object().command_set.all()]
#         # print kwargs
#         if form_class is None:
#             form_class = self.get_form_class()
#         return form_class(**kwargs)
#
#     def get_success_url(self):
#         obj = self.get_object()
#         return reverse('tournament_commands_list', kwargs={'tid': obj.id})
#
#     def post(self, request, *args, **kwargs):
#         form = self.get_form()
#         if form.is_valid():
#             commands = form.cleaned_data['commands']
#             print commands
#             return HttpResponseRedirect(self.get_success_url())
#         else:
#             return self.form_invalid(form)


class TourCommandCreateView(LoginRequiredMixinCustom, PermissionRequiredMixinCustom, CreateView):
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
        # return super(TourCommandCreateView, self).form_valid(form)

    def get_free_contestant(self):
        tournament_commands = Command.objects.filter(tournament__pk=self.kwargs['tid'])
        contestants = User.objects.filter(tournament__id=self.kwargs['tid'])\
            .exclude(contestant1__in=tournament_commands)\
            .exclude(command__in=tournament_commands)
        return contestants
        # return User.objects.filter(tournament__id=self.kwargs['tid'])

    def get_form(self, form_class=None):
        kwargs = self.get_form_kwargs()
        # tournament_commands = Command.objects.filter(tournament__pk=self.kwargs['tid'])
        # print tournament_commands
        contestatns = self.get_free_contestant()
        kwargs['initial']['contestants'] = [c for c in contestatns]
        # print kwargs
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**kwargs)


class TourCommandUpdateView(LoginRequiredMixinCustom, PermissionRequiredMixinCustom, UpdateView):
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
        contestatns = self.get_free_contestant()
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(**kwargs)
        choices = [(c.id, c) for c in contestatns]
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


class TourCommandDeleteView(LoginRequiredMixinCustom, PermissionRequiredMixinCustom, DeleteView):
    template_name = 'football_app/tournament_command_delete.html'
    model = Command
    pk_url_kwarg = 'comid'

    def get_success_url(self):
        command = Command.objects.get(pk=self.kwargs['comid'])
        messages.success(self.request, 'Command {} successful deleted!'.format(command))
        return reverse('tournament_commands_list', kwargs={'tid': command.tournament.id})
