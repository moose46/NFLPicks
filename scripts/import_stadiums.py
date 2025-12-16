import csv
from pathlib import Path

from mypicks.models import Stadium

# csv source file path
NFL_STADIUMS = Path(__file__).parent / "stadiums.csv"


def load_stadiums():
    with open(NFL_STADIUMS) as csvfile:
        reader = csv.DictReader(csvfile)
        for stadium in reader:
            print(stadium)
            s = Stadium()
            s.name = stadium["location"]
            s.save()


def run():
    load_stadiums()
