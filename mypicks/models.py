from datetime import datetime

from django.contrib.admin import display
from django.contrib.auth.models import User
from django.db import models


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

    class Meta:
        db_table = 'mypicks"."conference'


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

    class Meta:
        db_table = 'mypicks"."division'
        # unique_together = (("conference", "title"),)


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
        return f"{self.name} - {self.wins} - {self.losses} - {self.draws}"

    class Meta:
        db_table = 'mypicks"."team'
        # unique_together = (("name", "division"),)


class Game(Base):

    game_date: datetime = models.DateTimeField(
        "game_date",
        auto_now_add=False,
        default=datetime.now(),
    )
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
    away_team_points = models.IntegerField("away_team_points", default=0)
    home_team_points = models.IntegerField("home_team_points", default=0)

    def __str__(self):
        return f"{self.game_date.date()} - Home: {self.home_team.name} ({self.home_team_points}) - Away: {self.away_team.name} ({self.away_team_points})"

    class Meta:
        db_table = 'mypicks"."game'

        unique_together = (("game_date", "home_team", "away_team"),)
