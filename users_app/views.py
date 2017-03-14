from django.shortcuts import render
from django.contrib.auth.views import login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, UpdateView
from django.views.generic.edit import FormView
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from users_app.models import AvatarProfile
from users_app.forms import UserForm
from django.contrib.auth.models import Permission


class LoginRequiredMixinCustom(LoginRequiredMixin):
    login_url = "/users/auth/"
    # redirect_field_name = "next"
    raise_exception = False


class PermissionRequiredMixinCustom(PermissionRequiredMixin):
    permission_required = "auth.add_user"

    def get_redirect_field_name(self):
        """
        Override this method to override the redirect_field_name attribute.
        """
        messages.warning(self.request, "Please login as admin user for seeing the page you opened!")
        return self.redirect_field_name



class CabinetView(LoginRequiredMixinCustom, TemplateView):
    template_name='users_app/cabinet.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class UserUpdateView(LoginRequiredMixinCustom, UpdateView):
    model = User
    template_name = "users_app/user_update.html"
    pk_url_kwarg = 'uid'
    # success_url = '/users/cabinet/'
    # form_class = UserForm

    fields = ['email', 'username', 'first_name', 'last_name',]

    def get_success_url(self):
        return reverse('cabinet')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(reverse('cabinet'))
        if request.POST.get('email'):
            email = request.POST.get('email')
            user = User.objects.filter(email=email)
            if len(user) == 1 and user[0] != request.user:
                messages.error(request, "Some user already has typed email!")
                return HttpResponseRedirect(reverse('user_update', kwargs={'uid':request.user.id}))
        if request.POST.getlist('clear_avatar'):
            avatarprofile = AvatarProfile.objects.get(user=request.user)
            avatarprofile.delete()
        if request.FILES.get('avatar'):
            avatar = request.FILES.get('avatar')
            try:
                avatarprofile = AvatarProfile.objects.get(user=request.user)
            except AvatarProfile.DoesNotExist:
                AvatarProfile.objects.create(user=request.user, avatar=avatar)
            else:
                avatarprofile.avatar = avatar
                avatarprofile.save()
        return super(UserUpdateView, self).post(request, *args, **kwargs)
