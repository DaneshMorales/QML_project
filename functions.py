### This file contains all the useful functions to extract MLB data using the mlbstatsapi library


import mlbstatsapi
mlb = mlbstatsapi.Mlb()
import numpy as np
import pandas as pd

mlb_teams = [
    "Los Angeles Angels",
    "Houston Astros",
    "Athletics",
    "Toronto Blue Jays",
    "Atlanta Braves",
    "Milwaukee Brewers",
    "St. Louis Cardinals",
    "Chicago Cubs",
    "Arizona Diamondbacks",
    "Los Angeles Dodgers",
    "San Francisco Giants",
    "Cleveland Guardians",
    "Seattle Mariners",
    "Miami Marlins",
    "New York Mets",
    "Washington Nationals",
    "Baltimore Orioles",
    "San Diego Padres",
    "Philadelphia Phillies",
    "Pittsburgh Pirates",
    "Texas Rangers",
    "Tampa Bay Rays",
    "Boston Red Sox",
    "Cincinnati Reds",
    "Colorado Rockies",
    "Kansas City Royals",
    "Detroit Tigers",
    "Minnesota Twins",
    "Chicago White Sox",
    "New York Yankees"
]


hitting_stats = [
    "avg",
    "obp",
    "slg",
    "ops",
    "babip",
]


pitching_stats = [
    "era",
    "whip",
    "strikeoutwalkratio",
    "strikeoutsper9inn",
    "walksper9inn",
    "hitsper9inn",
    "runsscoredper9",
    "homerunsper9",
]



team_ids = [mlb.get_team_id(team_name= name)[0] for name in mlb_teams]

teams = {}

for id in team_ids:
    teams[mlb.get_team(id).abbreviation] = id


def get_player_era(player_name): ## Returns the ERA of a given pitcher in 2025
    player_id = mlb.get_people_id(player_name)[0]
    return float(mlb.get_player_stats(player_id, stats=['season'], groups=['pitching'], season=2025)['pitching']['season'].splits[0].stat.era)

def innings(innings_pitched_str): ## Converts innings pitched from string format to float format
    if '.' in innings_pitched_str:
        whole, fraction = innings_pitched_str.split('.')
        return int(whole) + int(fraction) / 3
    else:
        return int(innings_pitched_str)
    
def pitcher_era_home_and_away(game_id): ## Returns the ERA of the starting pitchers for both teams in a given game_id
    box = mlb.get_game_box_score(game_id = game_id)
    home_innings = 0
    away_innings = 0
    key_home = None
    key_away = None
    for key in box.teams.home.players.keys():
        if box.teams.home.players[key].stats['pitching'] != {}:
            if innings(box.teams.home.players[key].stats['pitching']['inningspitched']) > home_innings:
                home_innings = innings(box.teams.home.players[key].stats['pitching']['inningspitched'])
                key_home = key
    for key in box.teams.away.players.keys():
        if box.teams.away.players[key].stats['pitching'] != {}:
            if innings(box.teams.away.players[key].stats['pitching']['inningspitched']) > away_innings:
                away_innings = innings(box.teams.away.players[key].stats['pitching']['inningspitched'])
                key_away = key
    if key_home is not None and key_away is not None:
        home_era = np.round(box.teams.home.players[key_home].stats['pitching']['earnedruns'] / home_innings * 9, decimals=2)
        away_era = np.round(box.teams.away.players[key_away].stats['pitching']['earnedruns'] / away_innings * 9, decimals=2)
        return home_era, away_era
    

def get_2025_hitting_stats(team_abbreviation: str, hitting_stats: list): ## Returns a dictionary of hitting stats for a given team in 2025
    team_id = teams[team_abbreviation]
    team_stats = mlb.get_team_stats(team_id, stats=["season"] , groups=["hitting"], **{"season": 2025})
    return {stat: float(getattr(team_stats['hitting']['season'].splits[0].stat, stat)) for stat in hitting_stats}

def get_2025_pitching_stats(team_abbreviation: str, pitching_stats: list): ## Returns a dictionary of pitching stats for a given team in 2025
    team_id = teams[team_abbreviation]
    team_stats = mlb.get_team_stats(team_id, stats=["season"] , groups=["pitching"], **{"season": 2025})
    return {stat: float(getattr(team_stats['pitching']['season'].splits[0].stat, stat)) for stat in pitching_stats}


# Takes in game_id and list of pitching parameters to pull from box score. 
# Returns dataframe of home and away team pitching stats for those parameters.
def get_game_pitch_data(game_id, pitching_params):
    box_score = mlb.get_game_box_score(game_id)
    
    home_abb = box_score.teams.home.team.abbreviation
    away_abb = box_score.teams.away.team.abbreviation
    home_team_pitching = box_score.teams.home.teamstats["pitching"]
    away_team_pitching = box_score.teams.away.teamstats["pitching"]

    data = []
    for param in pitching_params:
        data.append({
            "Stat": param,
            f"{home_abb}": home_team_pitching.get(param),
            f"{away_abb}": away_team_pitching.get(param)
        })

    df = pd.DataFrame(data)
    print(df.to_string(index=False))

# Takes in game_id and list of batting parameters to pull from box score. 
# Returns dataframe of home and away team pitching stats for those parameters.
def get_game_bat_data(game_id, batting_param): 
    box_score = mlb.get_game_box_score(game_id)
    
    home_abb = box_score.teams.home.team.abbreviation
    away_abb = box_score.teams.away.team.abbreviation
    home_team_batting = box_score.teams.home.teamstats["batting"]
    away_team_batting = box_score.teams.away.teamstats["batting"]

    data = []
    for param in batting_param:
        data.append({
            "Stat": param,
            f"{home_abb}": home_team_batting.get(param),
            f"{away_abb}": away_team_batting.get(param)
        })

    df = pd.DataFrame(data)
    print(df.to_string(index=False))