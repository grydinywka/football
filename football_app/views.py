from django.shortcuts import render
from django.views.generic import TemplateView
from users_app.views import LoginRequiredMixinCustom


class TournamentView(LoginRequiredMixinCustom, TemplateView):
    template_name='football_app/index.html'
