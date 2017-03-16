from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

ALL_RATE = 100 # %
PART_RATE = 30 # %
MAX_VALUE_RATE = 1000


class AvatarProfile(models.Model):
    """To keep avatar of user"""
    user = models.OneToOneField(User)

    class Meta(object):
        verbose_name = u"Avatar of User"

    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name='AvataR')

    def __unicode__(self):
        return self.user.email


class RateUser(models.Model):
    user = models.OneToOneField(User)

    rate = models.IntegerField(null=True)

    def __unicode__(self):
        return self.user.email.__str__() + " Rate: " + self.rate.__str__()

    def save(self, *args, **kwargs):
        if self.rate < 0:
            self.rate = 0
        if self.rate > MAX_VALUE_RATE:
            self.rate = MAX_VALUE_RATE

        super(RateUser, self).save(*args, **kwargs)

    @staticmethod
    def calc_rate_first():
        rateusers = RateUser.objects.all().order_by('rate')
        if rateusers.count() == 0:
            return 300
        place = rateusers.count() * PART_RATE / ALL_RATE

        return rateusers[place].rate

    @property
    def user_pk(self):
        return self.user.pk