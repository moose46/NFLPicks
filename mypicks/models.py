from datetime import datetime

import pytz.reference
from django.contrib.admin import display
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class Base(models.Model):
    createdAt = models.DateTimeField("date_created", auto_now_add=True)
    updatedAt = models.DateTimeField("date_updated", auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        abstract = True


class Conference(Base):
    title = models.CharField("title", max_length=100, unique=True)
    description = models.TextField("description", blank=True)

    def __str__(self):
        return self.title

    # class Meta:
    #     db_table = 'mypicks2"."conference'


class Division(Base):
    title = models.CharField(
        "title",
        max_length=100,
        unique=False,
    )
    description = models.TextField("description", blank=True)
    conference = models.ForeignKey(
        Conference,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.conference.description} - {self.title}"

    # class Meta:
    # db_table = 'mypicks2"."division'
    # unique_together = (("conference", "title"),)bears


#
#
class Team(Base):
    name = models.CharField("name", max_length=100, unique=True)
    description = models.TextField("description", blank=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, default=1)
    wins = models.IntegerField("wins", default=0)
    losses = models.IntegerField("losses", default=0)
    draws = models.IntegerField("draws", default=0)

    def __str__(self):
        return f"{self.name}"
        # return f"{self.name} - {self.wins} - {self.losses} - {self.draws}"

    # class Meta:
    #     db_table = 'mypicks2"."team'
    # unique_together = (("name", "division"),)


class Stadium(Base):
    name = models.CharField("name", max_length=100, unique=True)
    city = models.CharField("city", max_length=100, blank=True)
    state = models.CharField("state", max_length=100, blank=True)
    website = models.URLField("website", max_length=100, blank=True)

    # class Meta:
    #     db_table = 'mypicks2"."stadium'


class Game(Base):

    location = models.CharField("location", max_length=100, blank=True)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE, null=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, default=1)
    game_date: datetime = models.DateTimeField(
        "Date",
        auto_now_add=False,
        default=datetime.now(),
        # timezone=pytz.timezone("US/Eastern"),
    )
    round_number = models.IntegerField("Round Number", default=0)
    week_number = models.IntegerField("week_number", default=15)
    home_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="home_team", verbose_name="Home:"
    )
    away_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="away_team",
        verbose_name="Visiting:",
    )
    away_team_points = models.IntegerField("Score", default=0)
    home_team_points = models.IntegerField("Score", default=0)

    def __str__(self):
        return f"{self.game_date.astimezone(timezone.get_current_timezone()).strftime(
                "%Y-%m-%d %H:%M"
            )} - Home: {self.home_team.name} ({self.home_team_points}) - Away: {self.away_team.name} ({self.away_team_points})"

    class Meta:
        # db_table = 'mypicks2"."game'

        unique_together = (("game_date", "home_team", "away_team"),)
