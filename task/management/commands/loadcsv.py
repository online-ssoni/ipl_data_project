from django.core.management.base import BaseCommand, CommandError
from task.models import Matches, Deliveries
import csv
import os
import sys
from django.db import transaction
def write_matches():
    print("Writing to Matches table!")
    filepath = os.path.join(os.getcwd(), 'matches.csv')
    fptr = open(filepath)
    csvfile = csv.reader(fptr)
    count = 1
    for row in csvfile:
        if count is not 1:
            current_season = row[1] 
            current_city = row[2]
            current_date = row[3]
            current_team1 = row[4]
            current_team2 = row[5]
            current_toss_winner = row[6] 
            current_toss_decision = row[7]
            current_result = row[8]
            current_dl_applied = row[9]
            current_winner = row[10]
            current_win_by_runs = row[11]
            current_win_by_wickets = row[12]
            current_player_of_match = row[13]
            current_venue = row[14]
            current_umpire1 = row[15]
            current_umpire2 = row[16]
            current_umpire3 = row[17]

            q = Matches(
                season = current_season
                ,city = current_city
                ,date = current_date
                ,team1 = current_team1
                ,team2 = current_team2
                ,toss_winner = current_toss_winner
                ,toss_decision = current_toss_decision
                ,result = current_result
                ,dl_applied = current_dl_applied
                ,winner = current_winner
                ,win_by_runs = current_win_by_runs
                ,win_by_wickets = current_win_by_wickets
                ,player_of_match = current_player_of_match
                ,venue = current_venue
                ,umpire1 = current_umpire1
                ,umpire2 = current_umpire2
                ,umpire3 = current_umpire3
            )
            q.save()
        else:
            count = count - 1

@transaction.atomic
def write_deliveries():
    print("Writing to Deliveries table!")
    filepath = os.path.join(os.getcwd(), 'deliveries.csv')
    fptr = open(filepath)
    csvfile = csv.reader(fptr)
    count = 1
    for row in csvfile:
        if count is not 1:
            current_match_id = Matches.objects.get(pk=row[0])
            current_inning = row[1]
            current_batting_team = row[2]  
            current_bowling_team = row[3]
            current_over = row[4]
            current_ball = row[5]
            current_batsman = row[6]
            current_non_striker = row[7]
            current_bowler = row[8]
            current_is_super_over = row[9]
            current_wide_runs = row[10]
            current_bye_runs = row[11]
            current_legbye_runs = row[12]
            current_noball_runs = row[13]
            current_penalty_runs = row[14]
            current_batsman_runs = row[15]
            current_extra_runs = row[16]
            current_total_runs = row[17]
            current_player_dismissed = row[18]
            current_dismissal_kind = row[19]
            current_fielder = row[20]

            q = Deliveries(
                match_id = current_match_id
                ,inning = current_inning
                ,batting_team = current_batting_team
                ,bowling_team = current_bowling_team
                ,over = current_over
                ,ball = current_ball
                ,batsman = current_batsman
                ,non_striker = current_non_striker
                ,bowler = current_bowler
                ,is_super_over = current_is_super_over
                ,wide_runs = current_wide_runs
                ,bye_runs = current_bye_runs
                ,legbye_runs = current_legbye_runs
                ,noball_runs = current_noball_runs
                ,penalty_runs = current_penalty_runs
                ,batsman_runs = current_batsman_runs
                ,extra_runs = current_extra_runs
                ,total_runs = current_total_runs
                ,player_dismissed = current_player_dismissed
                ,dismissal_kind = current_dismissal_kind
                ,fielder = current_fielder
            )
            q.save()
        else:
            count = count - 1
    transaction.commit()
    print("Database entries saved!")

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write("Writing to database!")
        # write_matches()
        # write_deliveries()
        print("Uncomment the functions to make it work (It might be dangerous!)")
