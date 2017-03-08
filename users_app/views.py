from django.shortcuts import render
from django.contrib.auth.views import login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class CabinetView(LoginRequiredMixin, TemplateView):
    template_name='users_app/cabinet.html'

    login_url = "/users/login/"
    # redirect_field_name = "next"
    raise_exception = False

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)