# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django.db.models.signals import post_save, post_delete, m2m_changed, pre_delete

from django.dispatch import receiver, Signal

from django.contrib.auth.models import User
from users_app.models import RateUser


@receiver(post_save, sender=User)
def create_user(sender, **kwargs):
    user = kwargs['instance']
    if kwargs['created']:
        rate = RateUser.calc_rate_first()
        RateUser.objects.create(user=user, rate=rate)
