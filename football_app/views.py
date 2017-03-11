from random import randint

from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView,\
                                 UpdateView, CreateView, FormView, RedirectView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from users_app.views import LoginRequiredMixinCustom, PermissionRequiredMixinCustom
from football_app.models import Tournament, Command, Round, Game
from football_app.forms import CreateToutnamentForm


class TournamentView(LoginRequiredMixinCustom, ListView):
    template_name='football_app/index.html'
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


class TournamentUpdateView(UpdateView):
    pk_url_kwarg = 'tid'
    template_name = 'football_app/tournament_update.html'
    model = Tournament

    fields = ('rounds', 'users', 'status')


class TournamentCreateView(CreateView):
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


class FormTeamsView(RedirectView):
    def form_teams(self, tournament, request, tourn_id):
        contestants = tournament.users.all().order_by('rateuser__rate', 'id')
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

            messages.info(request, "Teams for tournament #{} were formed!".format(tourn_id))

    def get(self, request,  *args, **kwargs):
        tourn_id = request.GET.get('tournament')
        if tourn_id:
            tournament = Tournament.objects.get(pk=tourn_id)
            self.url = reverse('tournament_detail', kwargs={'tid':tourn_id})
            self.form_teams(tournament, request, tourn_id)
            # print "WWWWWWWWWWWWWWWWWWWWWWWWWWWW " + tournament.__str__()

        else:
            self.url = reverse('home')
        return super(FormTeamsView, self).get(request,  *args, **kwargs)

