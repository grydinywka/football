from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.models import User

from .models import AvatarProfile, RateUser


class AvatarProfileInline(admin.StackedInline):
    model = AvatarProfile


class UserAdmin(auth_admin.UserAdmin):
    inlines = (AvatarProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(RateUser)
