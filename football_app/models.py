from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

IS_NOT_STARTED = 1
CURRENT = 2
ENDED = 3

CHAMPIONSHIP = 1
PLAYOFF =2


class Tournament(models.Model):
    """
        Tournament contains rounds and contestants and status
    """

    rounds = models.ManyToManyField('football_app.Round', blank=True, default=None)
    users = models.ManyToManyField(User, blank=True, default=None)
    title = models.CharField(blank=False, max_length=255, null=True)

    statuses = (
        (IS_NOT_STARTED, 'is not started'),
        (CURRENT, 'current'),
        (ENDED, 'ended'),
    )
    status = models.PositiveSmallIntegerField(blank=False, null=True, default=IS_NOT_STARTED, choices=statuses)

    def __unicode__(self):
        return "{} - Tournament #{}".format(self.title ,self.pk)


class Command(models.Model):
    """
        Command contains two contestants
    """

    tournament = models.ForeignKey("football_app.Tournament", blank=False, null=True, default=None)
    contestant1 = models.ForeignKey(User, blank=False, null=True, default=None, related_name='contestant1')
    contestant2 = models.ForeignKey(User, blank=False, null=True, default=None)

    def __unicode__(self):
        name1 = self.contestant1.last_name or 'first_name'
        name2 = self.contestant2.last_name or 'first_name'
        if len(self.contestant1.first_name) != 0:
            name1 += ' ' + self.contestant1.first_name[0] + '.'
        if len(self.contestant2.first_name) != 0:
            name2 += ' ' + self.contestant2.first_name[0] + '.'
        return "{} + {}".format(name1, name2)


class Round(models.Model):
    """
        Round model contains kind, games, description
    """

    kinds = (
        (CHAMPIONSHIP, 'championship'),
        (PLAYOFF, 'play-off'),
    )
    kind = models.PositiveSmallIntegerField(blank=False, null=True, default=CHAMPIONSHIP, choices=kinds)
    games = models.ManyToManyField('football_app.Game', blank=True, default=None)
    description = models.CharField(blank=False, null=True, default=None, max_length=256)

    def __unicode__(self):
        return self.description


class Game(models.Model):
    """
        Game model for creating contest between pair of commands.
    """

    command1 = models.ForeignKey("football_app.Command", blank=False, null=True, default=None, related_name='command1')
    command2 = models.ForeignKey("football_app.Command", blank=False, null=True, default=None)

    score1 = models.PositiveSmallIntegerField(blank=True, null=True, default=None)
    score2 = models.PositiveSmallIntegerField(blank=True, null=True, default=None)

    statuses = (
        (IS_NOT_STARTED, 'is not started'),
        (ENDED, 'ended'),
    )
    status = models.PositiveSmallIntegerField(blank=False, null=True, default=IS_NOT_STARTED, choices=statuses)

    def __unicode__(self):
        if self.status == IS_NOT_STARTED:
            score = "? - ?"
        elif self.status == ENDED:
            score = "{} - {}".format(self.score1, self.score2)
        return "{} {} {}".format(self.command1, score, self.command2)
