from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView,\
                                 UpdateView, CreateView, FormView,\
                                 RedirectView, DeleteView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from users_app.views import LoginRequiredMixinCustom, PermissionRequiredMixinCustom
from football_app.models import Tournament, Command, Round, Game,\
    IS_NOT_STARTED, CURRENT, ENDED,\
    CHAMPIONSHIP, PLAYOFF_1_16, PLAYOFF_1_8, PLAYOFF_1_4,\
    PLAYOFF_1_2, PLAYOFF_1_1, PLAYOFF_3, Voting, VotingList
from users_app.models import MAX_VALUE_RATE
from football_app.forms import ChampionshipGamesGenerateForm, VotingCloseForm


class VotingListCreateView(LoginRequiredMixinCustom, PermissionRequiredMixinCustom,
                           CreateView):

    """
        The view for creating voting of a tournament with status ENDED
    """
    template_name = "football_app/voting/voting_create.html"
    model = VotingList
    fields = ('tournament',)

    def get_success_url(self):
        messages.info(self.request, "VotingList was created")
        return reverse("cabinet")

    def get_form(self, form_class=None):
        kwargs = self.get_form_kwargs()
        tournaments = Tournament.objects.filter(status=ENDED)
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(**kwargs)
        choices = [(t.id, t) for t in tournaments]
        form.fields['tournament']._set_choices(choices)
        return form


class VotingBySortView(LoginRequiredMixinCustom, DetailView):
    """
        The view for voting - contestant vote for other contestants by sorting list
    """
    template_name="football_app/voting/voting_by_sort.html"
    pk_url_kwarg = 'tid'
    model = Tournament

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            voted_pks = request.POST.getlist("pks")
            # for pk in voted_pks:
            votinlist = self.get_object().votinglist
            voting = self.get_voting()
            if not voting.is_voted:
                point = len(voted_pks)
                index = 0
                while index < len(voted_pks):
                    pk = voted_pks[index]
                    votinlist.list["contestants"][pk]["point"] += point
                    index += 1
                    point -= 1
                # for pk in voted_pks:
                #     votinlist.list["contestants"][pk]["point"] = 0
                votinlist.save()
                voting.is_voted = True
                voting.save()
            return JsonResponse({"status": "Your vote is received!"})
        return HttpResponseRedirect(reverse('home'))

    def get_voting(self):
        votinlist = self.get_object().votinglist
        voting = self.request.user.voting_set.get(voting_list=votinlist)
        return voting

    def get(self, request, *args, **kwargs):
        if self.get_voting().is_voted:
            messages.info(request, "You are already voted for {}".format(self.get_object()))
            return HttpResponseRedirect(reverse('cabinet'))
        return super(VotingBySortView, self).get(request, *args, **kwargs)


class VotingClose(LoginRequiredMixinCustom, PermissionRequiredMixinCustom,
                  FormView):
    """
        The view for closing voting. After closing it will calculate rates of all contestants
    """
    template_name = "football_app/voting/voting_closing.html"
    form_class = VotingCloseForm

    def get_success_url(self):
        return reverse("cabinet")

    def calc_rate(self, votinglist):
        points = votinglist.list['contestants']
        votings  = votinglist.voting_set.all()
        if votings.count() > 0:

            max_point = 0
            for pk in points:
                if max_point < points[pk]['point']:
                    max_point = points[pk]['point']
            # print max_point
            if max_point != 0:
                norma = MAX_VALUE_RATE / max_point
                for voting in votings:
                    contestant = voting.contestant
                    rateuser = contestant.rateuser
                    rateuser.rate = points[str(contestant.pk)]['point']*norma
                    rateuser.save()

                # for contestants which do not belong to the tournament
                rest_contestants = User.objects.all().exclude(voting__in=votings)
                for contestant in rest_contestants:
                    rateuser = contestant.rateuser
                    rateuser.rate /= 2
                    rateuser.save()


    def form_valid(self, form):
        tournament = form.cleaned_data['tournament']
        votinglist = VotingList.objects.get(tournament__pk=tournament)
        votinglist.is_open = False
        votinglist.save()
        self.calc_rate(votinglist)
        messages.info(self.request,"Voting for {} is closed".format(tournament))
        return HttpResponseRedirect(self.get_success_url())

