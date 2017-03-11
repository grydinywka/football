"""football URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy

from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from users_app.views import CabinetView, UserUpdateView
from football_app.views import TournamentView, TournamentDetailView,\
    TournamentUpdateView, TournamentCreateView, FormTeamsView

from registration.backends.simple.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TournamentView.as_view(), name='home'),
    url(r'^tournament/(?P<tid>\d+)/detail/$', TournamentDetailView.as_view(), name="tournament_detail"),
    url(r'^tournament/(?P<tid>\d+)/update/$', TournamentUpdateView.as_view(), name="tournament_update"),
    url(r'^tournament/create/$', TournamentCreateView.as_view(), name="tournament_create"),
    url(r'^tournament/form_team/$', FormTeamsView.as_view(), name="form_teams"),

    # User Related urls
    url(r'^users/auth/$', TemplateView.as_view(template_name='users_app/authpage.html'), name='authpage'),
    url(r'^users/cabinet/$', CabinetView.as_view(), name='cabinet'),
    url(r'^users/cabinet/(?P<uid>\d+)/edit$', UserUpdateView.as_view(), name='user_update'),
    url(r'^users/logout/$', auth_views.logout, kwargs={'next_page':'authpage'}, name='auth_logout'),
    url(r'^users/register/$', RegistrationView.as_view(form_class=RegistrationFormUniqueEmail), name='registration_register'),
    url(r'^register/complete/$', RedirectView.as_view(pattern_name='cabinet'), name='registration_complete'),
    url(r'^users/', include('registration.backends.simple.urls', namespace='users')),

    # socials
    url('^social/', include('social_django.urls', namespace='social')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
