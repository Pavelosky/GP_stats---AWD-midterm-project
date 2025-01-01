import os
import sys
import django
import csv
from datetime import timedelta

# Set up Django
sys.path.append("C:/Users/pawel/OneDrive/Documenten/BSc CS UoL/level 6/AWD/mid-term/GP_Stats") 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GP_stats.settings") 
django.setup()

from mrds.models import *

# Path to the CSV file
data_file = "motogpresultdataset.csv" 

# Clear existing data to avoid duplicates
Result.objects.all().delete()
Race.objects.all().delete()
Rider.objects.all().delete()
Team.objects.all().delete()
Circuit.objects.all().delete()

# Create dictionaries to store unique entries for related tables
circuits = {}
riders = {}
teams = {}
races = {}

# Open and process the CSV file
with open(data_file, newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    for row in csv_reader:
        # Handle Circuit
        circuit_key = row['shortname']
        if circuit_key not in circuits:
            circuit = Circuit.objects.create(
                shortname=row['shortname'],
                circuit_name=row['circuit_name']
            )
            circuits[circuit_key] = circuit
        
        # Handle Rider
        rider_key = row['rider']
        if rider_key not in riders:
            rider = Rider.objects.create(
                id=row['rider'],  # Assuming rider is a unique identifier
                name=row['rider_name'],
                country=row['country'],
                number=row['number']
            )
            riders[rider_key] = rider
        
        # Handle Team
        team_key = row['team_name']
        if team_key not in teams:
            team = Team.objects.create(
                name=row['team_name'],
                bike_name=row['bike_name']
            )
            teams[team_key] = team
        
        # Handle Race
        race_key = (row['year'], row['category'], row['sequence'])
        if race_key not in races:
            race = Race.objects.create(
                year=row['year'],
                category=row['category'],
                sequence=row['sequence'],
                circuit=circuits[circuit_key]
            )
            races[race_key] = race
        else:
            race = races[race_key]
        
        # # Convert time string to timedelta
        # time_str = row['time']
        # # Time behind the winner
        # if time_str.startswith('+'):
        #     time_str = time_str[1:]
        #     if "'" in time_str:
        #         minutes, rest = time_str.split("'")
        #         seconds, milliseconds = map(float, rest.split('.'))
        #         time_delta = timedelta(minutes=int(minutes), seconds=int(seconds), milliseconds=int(milliseconds * 1000))
        #     else:
        #         seconds, milliseconds = map(float, time_str.split('.'))
        #         time_delta = timedelta(seconds=int(seconds), milliseconds=int(milliseconds * 1000))
        # # Rider didn't finish the race
        # elif 'Laps' or 'Lap' in time_str:
        #     time_delta = None
        # # Time for the race winner
        # else:
        #     time_parts = time_str.split("'")
        #     minutes = int(time_parts[0])
        #     seconds, milliseconds = map(float, time_parts[1].split('.'))
        #     time_delta = timedelta(minutes=minutes, seconds=int(seconds), milliseconds=int(milliseconds * 1000))

        # Handle missing speed
        speed = row['speed']
        if speed == '':
            speed = None
        else:
            speed = float(speed)

        # Handle Result
        Result.objects.create(
            race=race,
            rider=riders[rider_key],
            team=teams[team_key],
            position=row['position'],
            points=row['points'],
            speed=speed,
            time=row['time']
        )

print("Database successfully populated!")
