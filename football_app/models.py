from __future__ import unicode_literals

from jsonfield import JSONField

from django.db import models
from django.contrib.auth.models import User

IS_NOT_STARTED = 1
CURRENT = 2
ENDED = 3

CHAMPIONSHIP = 1
PLAYOFF_1_16 = 2
PLAYOFF_1_8 = 3
PLAYOFF_1_4 = 4
PLAYOFF_1_2 = 5
PLAYOFF_1_1 = 6
PLAYOFF_3 = 7


class Tournament(models.Model):
    """
        Tournament contains rounds and contestants and status
    """

    championship = models.OneToOneField(
        'football_app.Round',
        blank=True,
        null=True,
        default=None,
        related_name='tournament_chip',
        on_delete=models.SET_NULL
    )
    playoff = models.OneToOneField(
        'football_app.Round',
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_NULL
    )
    contestants = models.ManyToManyField(User, blank=True, default=None)
    title = models.CharField(blank=False, max_length=255, null=True)

    statuses = (
        (IS_NOT_STARTED, 'is not started'),
        (CURRENT, 'current'),
        (ENDED, 'ended'),
    )
    status = models.PositiveSmallIntegerField(blank=False, null=True, default=IS_NOT_STARTED, choices=statuses)

    def __unicode__(self):
        return "{} - Tournament #{}".format(self.title ,self.pk)

    @property
    def get_status(self):
        return self.statuses[self.status-1][1]


class Command(models.Model):
    """
        Command contains two contestants
    """
    title = models.CharField(blank=True, max_length=255, null=True, default=None)
    tournament = models.ForeignKey("football_app.Tournament", blank=False, null=True, default=None)
    contestant1 = models.ForeignKey(User, blank=False, null=True, default=None, related_name='contestant1')
    contestant2 = models.ForeignKey(User, blank=False, null=True, default=None)

    def __unicode__(self):
        if self.title:
            return self.title
        else:
            name1 = self.contestant1.last_name or 'first_name'
            name2 = self.contestant2.last_name or 'first_name'
            if len(self.contestant1.first_name) != 0:
                name1 += ' ' + self.contestant1.first_name[0] + '.'
            if len(self.contestant2.first_name) != 0:
                name2 += ' ' + self.contestant2.first_name[0] + '.'
            return "{} + {}".format(name1, name2)

    def is_contestant(self, contestant):
        if contestant == self.contestant1 or contestant == self.contestant2:
            return True
        return False

    @property
    def get_contestants(self):
        return [self.contestant1, self.contestant2]

    def get_played_games_chip(self):
        return self.game_command1.filter(kind=CHAMPIONSHIP, status=ENDED),\
               self.game_set.filter(kind=CHAMPIONSHIP, status=ENDED)

    def get_played_games_chip_count(self):
        games = self.get_played_games_chip()[0].count() +\
            self.get_played_games_chip()[1].count()
        return games

    def get_played_games_playoff(self):
        games = self.game_command1.exclude(kind=CHAMPIONSHIP).count() +\
            self.game_set.exclude(kind=CHAMPIONSHIP).count()
        return games

    def get_wins_chip(self):
        wins = 0
        for game in self.get_played_games_chip()[0]:
            if game.score1 > game.score2:
                wins += 1
        for game in self.get_played_games_chip()[1]:
            if game.score1 < game.score2:
                wins += 1
        return wins

    def get_defeats_chip(self):
        defeats = 0
        for game in self.get_played_games_chip()[0]:
            if game.score1 < game.score2:
                defeats += 1
        for game in self.get_played_games_chip()[1]:
            if game.score1 > game.score2:
                defeats += 1
        return defeats

    def goals_goals_against(self):
        goals = 0
        goals_against = 0
        for game in self.get_played_games_chip()[0]:
            goals += game.score1
            goals_against += game.score2
        for game in self.get_played_games_chip()[1]:
            goals += game.score2
            goals_against += game.score1
        return goals, goals_against



class Round(models.Model):
    """
        Round model contains kind, games, description
    """

    games = models.ManyToManyField('football_app.Game', blank=True, default=None)
    description = models.CharField(blank=False, null=True, default=None, max_length=256)

    def __unicode__(self):
        return self.description


class Game(models.Model):
    """
        Game model for creating contest between pair of commands.
    """

    command1 = models.ForeignKey("football_app.Command", blank=False, null=True, default=None,
                                 related_name='game_command1')
    command2 = models.ForeignKey("football_app.Command", blank=False, null=True, default=None)

    score1 = models.PositiveSmallIntegerField(blank=True, null=True, default=None)
    score2 = models.PositiveSmallIntegerField(blank=True, null=True, default=None)

    statuses = (
        (IS_NOT_STARTED, 'is not started'),
        (CURRENT, 'current'),
        (ENDED, 'ended'),
    )
    status = models.PositiveSmallIntegerField(blank=False, null=True, default=IS_NOT_STARTED, choices=statuses)

    kinds = (
        (CHAMPIONSHIP, 'championship'),
        (PLAYOFF_1_16, 'play-off-1/16'),
        (PLAYOFF_1_8, 'play-off-1/8'),
        (PLAYOFF_1_4, 'play-off-1/4'),
        (PLAYOFF_1_2, 'play-off-1/2'),
        (PLAYOFF_1_1, 'play-off-final'),
        (PLAYOFF_3, 'play-off-third-place'),
    )
    kind = models.PositiveSmallIntegerField(blank=False, null=True, default=CHAMPIONSHIP, choices=kinds)

    def __unicode__(self):
        if self.status == IS_NOT_STARTED:
            score = "? - ?"
        elif self.status == ENDED:
            score = "{} - {}".format(self.score1, self.score2)
        elif self.status == CURRENT:
            score = "{} - {}(now is playing)".format(self.score1, self.score2)
        return "{} {} {}".format(self.command1, score, self.command2)


class VotingList(models.Model):
    tournament = models.OneToOneField(Tournament, blank=False, null=True,
                                      default=None,
                                      on_delete=models.SET_NULL)
    is_open = models.BooleanField(blank=False, default=True)
    list = JSONField(blank=True)

    def __unicode__(self):
        return "VotingList for tournament #{}".format(self.tournament.id)

    def save(self, *args, **kwargs):
        if self.pk is None:
            d_cont = {}
            for contestant in self.tournament.contestants.all():
                d_cont[contestant.id.__str__()] = {'point': 0}
            self.list = {'contestants' : d_cont}

        super(VotingList, self).save(*args, **kwargs)

class Voting(models.Model):
    """model for voting by certain tournament"""
    class Meta:
        unique_together = ('contestant', 'voting_list',)

    contestant = models.ForeignKey(User, blank=False, null=True, default=None)
    is_voted = models.BooleanField(blank=False, default=False)
    # final_place = models.PositiveSmallIntegerField(blank=True, null=True, default=None)
    voting_list = models.ForeignKey(VotingList, blank=False, null=True, default=None)

    def __unicode__(self):
        return "Voting for contestant #{} and tournament #{}".format(self.contestant.id, self.voting_list.tournament.id)

