from django.contrib import admin

# Register your models here.

from mypicks.models import Conference, Division, Team, Game


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("division", "name", "wins", "losses", "draws")
    ordering = ("-wins", "losses", "draws")
    list_filter = [
        "division",
    ]


#
#
@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    pass


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = [
        "game_date",
        "home_team",
        "home_team_points",
        "away_team",
        "away_team_points",
    ]
    ordering = ["-game_date"]
    fieldsets = (None,('fields':))