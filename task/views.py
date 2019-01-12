from django.shortcuts import render
from task.models import Matches, Deliveries
import csv
import os
import sys
from django.db import transaction
from django.db.models import Count, Sum, FloatField
from django.db.models.functions import Cast  
import json
from json import JSONEncoder
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


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

def format_data(match_winners):
    """Returns the formatted data to be able to be plotted on the chart"""
    formatted_match_winners = {}
    for winner in match_winners:
        year = winner[0]
        team = winner[1]
        matches_won = winner[2]

        if year in formatted_match_winners.keys():
            if team in formatted_match_winners[year].keys():
                current_matches_won = formatted_match_winners[year][team] + matches_won
            else:
                formatted_match_winners[year][team] = matches_won
        else:
            formatted_match_winners[year] = {team: matches_won}

    return formatted_match_winners

def get_team_list(seasons, winner_of_all_years):
    """Returns list of all teams"""
    team_list = []
    for year in seasons:
        current_teams = list(winner_of_all_years[year].keys())
        for team in current_teams:
            if team not in team_list and team is not "":
                team_list.append(team)
    return team_list

def get_team_data(team_reader, seasons, winner_of_all_years):
    """Returns winners of all seasons"""
    team_data = []
    for team in team_reader:
        current_team_data = []
        for season in seasons:
            if team in winner_of_all_years[season].keys():
                current_team_data.append(winner_of_all_years[season][team])
            else:
                current_team_data.append(0)
        team_data.append(current_team_data)
    return team_data

def get_all_teams(team_reader):
    """Returns list of all teams"""
    all_teams = []
    for team in team_reader:
        if team[0] not in all_teams:
            all_teams.append(team[0])
        if team[1] not in all_teams:
            all_teams.append(team[1])
    return all_teams

def get_team_match_played(team_name, team_reader):
    """Returns total matches played by each team"""
    total_matches_played = 0
    for teams in team_reader:
        if team_name in [teams[0], teams[1]]:
            total_matches_played = total_matches_played + 1
    return total_matches_played

def get_team_wins(team_name, team_reader):
    """Returns the total matches won by the team"""
    total_wins = 0
    for teams in team_reader:
        if teams[2] == team_name:
            total_wins = total_wins + 1
    return total_wins

def get_team_success(all_teams, team_reader):
    """Returns success rate of each team"""
    team_success = []
    for team in all_teams:
        team_name = team
        team_match_played = get_team_match_played(team_name, team_reader)
        team_wins = get_team_wins(team_name, team_reader)
        success_rate = (team_wins / team_match_played) * 100
        team_success.append({"team": team_name, "success_rate": success_rate})
    return team_success

def get_success_rates(team_success_reader):
    """Returns success rates of the team"""
    success_rates = []
    for teams in team_success_reader:
        current_success = float("{0:.2f}".format(teams["success_rate"]))
        success_rates.append(current_success)
    return success_rates

# @transaction.atomic
@cache_page(CACHE_TTL)
def index(request):
    # write_deliveries()
    # transaction.commit()
    # print("Database entries saved!")
    context = {}
    return render(request,'task/index.html', context)


@cache_page(CACHE_TTL)
def solution1(request):
    result = Matches.objects.values('season').annotate(count=Count('season'))
    seasons = []
    counts = []
    data = list(result)
    for row in data:
        seasons.append(row['season'])
        counts.append(row['count'])
    context = {'seasons':seasons, 'counts':counts}
    return render(request,'task/result1.html', context)

@cache_page(CACHE_TTL)
def solution2(request):
    result = Matches.objects.values('season', 'winner').annotate(count=Count('season')).order_by('season')
    match_winners = []
    for row in result:
        match_winners.append([row['season'], row['winner'], row['count']])
    winner_of_all_years = format_data(match_winners)
    seasons = list(winner_of_all_years.keys())
    team_list = get_team_list(seasons, winner_of_all_years)
    team_data = get_team_data(team_list, seasons, winner_of_all_years)
    context = {'seasons':seasons, 'team_data':team_data, 'team_list':team_list}
    return render(request,'task/result2.html', context)

@cache_page(CACHE_TTL)
def solution3(request):
    result = Deliveries.objects.values('bowling_team').annotate(runs=Sum('extra_runs')).filter(match_id__in = Matches.objects.filter(season='2016'))
    result = list(result)
    teams = []
    runs = []
    for row in result:
        teams.append(row['bowling_team'])
        runs.append(row['runs'])
    context = {'teams': json.dumps(teams), 'runs': json.dumps(runs)}
    return render(request,'task/result3.html', context)

@cache_page(CACHE_TTL)
def solution4(request):
    # For the year 2015 plot the top economical bowlers.
    result = Deliveries.objects.filter(match_id__in=Matches.objects.filter(season=2015)).values('bowler').annotate(economy=Cast(Sum('total_runs'), FloatField())/Cast(Count('over')/6, FloatField())).order_by('economy')[:5]
    result = list(result)
    bowlers = []
    economies = []
    for row in result:
        bowlers.append(row['bowler'])
        economies.append(row['economy'])
    context = {'bowler': json.dumps(bowlers), 'economy': json.dumps(economies)}
    return render(request,'task/result4.html', context)

@cache_page(CACHE_TTL)
def solution5(request):
    result = Matches.objects.values('team1','team2','winner')
    team_reader = []
    for row in result:
        team_reader.append(tuple(row.values()))
    all_teams = get_all_teams(team_reader)
    team_success = get_team_success(all_teams, team_reader)
    success_rates = get_success_rates(team_success)
    context = {'all_teams':all_teams, 'success_rates':success_rates}
    return render(request,'task/result5.html', context)
