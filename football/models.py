from django.db import models
from django.contrib.auth.models import User


class AvatarProfile(models.Model):
    """To keep avatar of user"""
    user = models.OneToOneField(User)

    class Meta(object):
        verbose_name = u"Avatar of User"

    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name='AvataR')

    def __unicode__(self):
        return self.user.email

