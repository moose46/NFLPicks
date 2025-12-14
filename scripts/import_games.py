import csv
import datetime
from datetime import timedelta, timezone
from sqlite3 import IntegrityError

# from django.utils import timezone
import pendulum
from mypicks.models import Game, Team
from pathlib import Path
import os
from zoneinfo import ZoneInfo

NFL_GAMES = Path(__file__).parent / "nfl-2025-UTC.csv"


def update_location(game, field_name):
    game.location = field_name
    game.save()


def add_game(new_game):
    print(f"Adding {new_game}")
    try:
        game = Game()
        game.location = new_game["Location"]
        game.game_date = datetime.datetime.strptime(new_game["Date"], "%d/%m/%Y %H:%M")
        # game.game_date = game.game_date.replace(tzinfo=timezone(timedelta(hours=-5)))
        game.week_number = new_game["Round Number"]
        # print(new_game["Home Team"])
        home_team = Team.objects.get(name__startswith=new_game["Home Team"])
        away_team = Team.objects.get(name__startswith=new_game["Away Team"])
        # print(f"Team = {home_team.id}")
        game.home_team = home_team
        game.away_team = away_team
        # print(f"Team = {new_game["Result"].split(sep='-')}")
        try:
            game.home_team_points = int(new_game["Result"].split(sep="-")[0])
            game.away_team_points = int(new_game["Result"].split(sep="-")[1])
        except ValueError as e:
            pass
        game.save()
        print(game)

    except IntegrityError as e:
        print(f"Game with {new_game} {e}.")
        exit()


def read_csv():
    with open(NFL_GAMES) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(row["Home Team"], row["Away Team"])
            try:
                home_team = Team.objects.get(name__startswith=row["Home Team"])
                away_team = Team.objects.get(name__startswith=row["Away Team"])
                game = Game.objects.filter(
                    home_team_id=home_team.id, away_team_id=away_team.id
                )
                if game:  # already entered into the database
                    if game[0].location == "":
                        print(game[0], row["Location"])
                        update_location(game[0], row["Location"])
                else:  # insert the game into the database
                    add_game(row)
                # for team in game:
                #     print(team)
                # print(
                #     f"{row["Date"]} Home Team: {home_team.name} - Away Team: {away_team.name}"
                # )
            except Team.DoesNotExist:
                print(row["Home Team"])
                exit()


def run():
    if not os.path.exists(NFL_GAMES):
        print(f"NFL_GAMES {NFL_GAMES} not found.")
        exit()
    read_csv()
