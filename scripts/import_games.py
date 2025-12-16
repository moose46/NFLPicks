import csv
import datetime
import pytz

# from datetime import timedelta, timezone
from sqlite3 import IntegrityError

from django.core.management import CommandError

from django.utils import timezone
from mypicks.models import Game, Team
from pathlib import Path
import os

# csv source file path
NFL_GAMES = Path(__file__).parent / "nfl-2025-UTC.csv"


def add_game(new_game: object) -> None:
    """
    Add a new game to the database
    :param new_game:
    :type new_game:
    """
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
            print(e)
            exit()
        game.save()
        # print(game)

    except IntegrityError as e:
        print(f"Error .......... Game with {new_game} {e}.")
        exit()


def read_csv():
    """
    Reads nfl csv file
    """
    with open(NFL_GAMES) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row["Home Team"], row["Away Team"])
            try:
                home_team = Team.objects.get(name__startswith=row["Home Team"])
                away_team = Team.objects.get(name__startswith=row["Away Team"])
                if (
                    Game.objects.filter(home_team=home_team.id)
                    .filter(away_team=away_team.id)
                    # https://studygyaan.com/django/runtimewarning-datetimefield-received-naive-datetime-in-django-python
                    .filter(
                        game_date=timezone.make_aware(
                            datetime.datetime.strptime(row["Date"], "%d/%m/%Y %H:%M"),
                            timezone=pytz.timezone("US/Eastern"),
                        )
                        # game_date=row["Date"]
                    )
                    .exists()
                ):
                    continue
                    # print(f"Error ........... {row}")
                    # return
                print(f"Inserting {row["Date"]} {row["Home Team"]}, {row["Away Team"]}")
                try:
                    add_game(row)
                except IntegrityError as e:
                    CommandError("Already in the Database", row)
                    print(e)
                    exit()
            except Team.DoesNotExist:
                print(f"Error ........... {row["Home Team"]}")
                exit()


def run():
    """
    checks for the csv file and updates the database
    :rtype: None
    """
    if not os.path.exists(NFL_GAMES):
        print(f"NFL_GAMES {NFL_GAMES} not found.")
        exit()
    read_csv()
