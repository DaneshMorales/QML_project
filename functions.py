import mlbstatsapi
mlb = mlbstatsapi.Mlb()

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

team_ids = [mlb.get_team_id(team_name= name)[0] for name in mlb_teams]

teams = {}

for id in team_ids:
    teams[mlb.get_team(id).abbreviation] = id


def get_player_era(player_name):
    player_id = mlb.get_people_id(player_name)[0]
    return mlb.get_player_stats(player_id, stats=['season'], groups=['pitching'], season=2025)['pitching']['season'].splits[0].stat.era