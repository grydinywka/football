# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django.db.models.signals import post_save, post_delete, m2m_changed, pre_delete

from django.dispatch import receiver, Signal

from django.contrib.auth.models import User
from football_app.models import VotingList, Voting


@receiver(post_save, sender=VotingList)
def create_user(sender, **kwargs):
    voting_list = kwargs['instance']
    if kwargs['created']:
        for contestant in voting_list.tournament.contestants.all():
            Voting.objects.create(contestant=contestant,
                                  voting_list=voting_list)
