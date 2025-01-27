import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import pickle
import re
import io
from datetime import datetime
import random
import os
import numpy as np
import json


class FBRefDataLoader:

    def __init__(self, data_directory):
        self.data_directory = data_directory

    def load_data(self, data, season):
        file_path = os.path.join(self.data_directory, season, f"{data}.json")
        with open(file_path, "r") as f:
            return json.load(f)
    
    def listdir(self, directory:str) -> list:
        return [x for x in os.listdir(os.path.join(self.data_directory, directory)) if x[0] != '.']

class FBRefDataWriter:

    def __init__(self, data_directory):
        self.data_directory = data_directory

    def write_data(self, data, season, file_name):
        file_path = os.path.join(self.data_directory, season, f"{file_name}.json")
        with open(file_path, "w") as f:
            return json.dump(data, f)


class FBRefDataFormatter:

    def __init__(self):
        self.a = True

    def add_team_name_to_player(self, player_details, team_details):
        for team_name, players_names_list in team_details.items():
            for player in players_names_list:
                if player in player_details.keys():
                    player_details[player]['Team'] = team_name
        for player in player_details.keys():
            player_details[player]['Name'] = player
        player_details = list(player_details.values())
        return player_details

    def split_match_data(self, match_report):
        match_data_list = [] 
        player_stats_list = [] 
        goalie_stats_list = []  
    
        for match in match_report:
            match_id = match["Match_ID"]
    
            match_data = {k: v for k, v in match.items() if k not in ["Home_Player_Stats", "Away_Player_Stats", "Home_Goalie_Stats", "Away_Goalie_Stats"]}
            match_data_list.append(match_data)
    
            home_player_stats = match["Home_Player_Stats"]
            away_player_stats = match["Away_Player_Stats"]
            for player in home_player_stats + away_player_stats:
                
                player["match_id"] = match_id  
                player["team_name"] = match_data["Home"] if player in home_player_stats else match_data["Away"]
                player_stats_list.append(player)
                
    
            home_goalie_stats = match["Home_Goalie_Stats"]
            away_goalie_stats = match["Away_Goalie_Stats"]
            for goalie in home_goalie_stats + away_goalie_stats:
                goalie["match_id"] = match_id  
                goalie["team_name"] = match_data["Home"] if player in home_player_stats else match_data["Away"]
                goalie_stats_list.append(goalie)
    
        return match_data_list, player_stats_list, goalie_stats_list



class FBRefExtractor:
    
    def __init__(self, **kwargs):
        self.fbref_url = "https://fbref.com{}"
        self.request_timestamps = list()
        if kwargs.get("season"):
            self.set_season(season)

    def set_season(self, season):
        self.season = season
        self.is_current_season = self.check_current_season()

    def check_current_season(self):
        start_year, end_year = map(int, self.season.split("-"))
        
        today = datetime.today()

        season_start = datetime(start_year, 8, 1)
        season_end = datetime(end_year, 5, 31)   

        return season_start <= today <= season_end

    def enforce_rate_limit(self):
        now = time.time()
        time.sleep(random.uniform(3,4))
        self.request_timestamps = [ts for ts in self.request_timestamps if now - ts <= 60]

        if len(self.request_timestamps) >= 16:
            wait_time = 60 - (now - self.request_timestamps[0])
            print(f"Waiting: {wait_time}")
            time.sleep(wait_time)
        self.request_timestamps.append(time.time())

    def construct_season_stats_endpoint(self):
        endpoint_stem = self.construct_season_endpoint()
        return endpoint_stem+"Premier-League-Stats"
    
    def construct_season_fixtures_endpoint(self):
        endpoint_stem = self.construct_season_endpoint()
        return endpoint_stem+"-Scores-and-Fixtures"
        
    def construct_season_endpoint(self, **kwargs):
        fixtures_path = "schedule" if kwargs.get("id") == "fixtures" else ""
        season_path = self.season if not self.is_current_season else ""
        stats_path = (self.season+"-" if not self.is_current_season else "")
        return f"/en/comps/9/{season_path}/{fixtures_path}/{stats_path}Premier-League"
                
    def make_request(self, endpoint: str) -> str:
        self.enforce_rate_limit()
        url = self.fbref_url.format(endpoint)
        while True:
            response = requests.get(url)
            if response.status_code == 429:  # Rate limited
                print("Rate limited. Pausing for 5 minutes...")
                print(response.text)
                time.sleep(300)  # Wait for 5 minutes
            else:
                return response.text

    def get_page_soup(self, url: str) -> BeautifulSoup:
        return BeautifulSoup(self.make_request(url), 'html.parser')

    def extract_team_links(self, season_endpoint: str) -> dict:
        league_teams_soup = self.get_page_soup(season_endpoint)
        league_table = league_teams_soup.select('table.stats_table')[0]
        teams_dict = {
            team_link.get_text(): team_link.get("href")
            for team_link in league_table.find_all('a') if "squads" in team_link.get("href")
        }
        return teams_dict

    def extract_player_links(self, team_endpoint: str) -> dict:
        team_soup = self.get_page_soup(team_endpoint)
        team_players_table = team_soup.select('table.stats_table')[0]
        players_links_dict = {
            l.get_text(): l.get("href")
            for l in team_players_table.find_all('a')
            if (link := l.get("href")) and "players" in link and "matchlogs" not in link
        }
        return players_links_dict

    def extract_player_details(self, player_endpoint: str) -> dict:
        player_soup = self.get_page_soup(player_endpoint)
        media_item_div = player_soup.select_one('div.media-item')
        image_src = media_item_div.find('img')['src'] if media_item_div else None
        player_data = dict()

        # Extracting data dynamically
        for p in player_soup.find_all('p'):
            text = p.get_text(strip=True)
            # Extract position and footed
            if "Position:" in text:
                position_part = text.split("▪")[0].strip()
                footed_part = text.split("▪")[1].strip() if "▪" in text else None
                player_data['position'] = position_part.split(":")[1].strip()
                if footed_part:
                    player_data['footed'] = footed_part.split(":")[1].strip()
            # Extract height and weight
            if "cm" in text and "kg" in text:
                height, weight = map(str.strip, text.split(',')[:2])
                player_data['height'] = height
                player_data['weight'] = weight.split('(')[0]
            # Extract date of birth and place of birth
            if "Born:" in text:
                birth_data = p.find("span", {"data-birth": True})
                if birth_data:
                    player_data['dob'] = birth_data["data-birth"]
                    birth_place = birth_data.find_next_sibling("span")
                    if birth_place:
                        player_data['birth_place'] = birth_place.get_text(strip=True)[3:]  # Clean prefix if necessary
            # Extract national team
            if "National Team:" in text:
                player_data['national_team'] = text.split(":")[1].strip()
            # Extract club
            if "Club:" in text:
                player_data['club'] = text.split(":")[1].strip()
            # Extract wages and contract expiry
            if "Wages" in text:
                wages = p.select_one('.important').get_text(strip=True) if p.select_one('.important') else None
                player_data['wages'] = wages
                if "Expires" in text:
                    contract_expires = text.split("Expires")[1].split(".")[0].strip()
                    player_data['contract_expiry'] = contract_expires
        if image_src:
            player_data['img'] = image_src
        return player_data

    def extract_match__report_links(self, fixtures):
        return None

    def get_fixtures(self, fixtures_endpoint: str) -> BeautifulSoup:
        fixtures_soup = self.get_page_soup(fixtures_endpoint)
        fixtures_table = fixtures_soup.find(id='all_sched')
        return fixtures_table

    def fixtures_to_dict(self, fixtures):
        fixtures_df = pd.read_html(io.StringIO(str(fixtures)))[0]
    
        fixtures_df = fixtures_df[fixtures_df['Wk'].notna()].reset_index(drop=True)
        fixtures_df[['Home_Score', 'Away_Score']] = fixtures_df['Score'].str.split('–', expand=True)
        fixtures_df['Wk'] = "GW" + fixtures_df['Wk'].astype(int).astype(str)
    
        fixtures_df = fixtures_df.rename(columns={'Wk':'GW', 'xG':"Home_Expected", 'xG.1':"Away_Expected", "Match Report":"Match_Report"})
        
        match_report_links = [l.get('href') for l in fixtures.find_all('a') if "Match Report" in l]
        match_report_links.extend([None]*(len(fixtures_df)-len(match_report_links)))
        fixtures_df["Match Report Link"] = match_report_links
        fixtures_df["Match_ID"] = f"{self.season}"+fixtures_df["GW"]+fixtures_df["Home"]+fixtures_df["Away"]
        fixtures_df["Match_Report"] = (fixtures_df["Match_Report"] == "Match Report")
        fixtures_df = fixtures_df.replace({np.nan: None})
        
        fixtures_dict = fixtures_df.to_dict(orient='records')
        return fixtures_dict

    def append_match_data(self, fixtures_dict):
        for count, match in enumerate(fixtures_dict):
            if match["Match_Report"]:
                home_player_stats, away_player_stats, home_goalie_stats, away_goalie_stats = self.get_match_data(match["Match Report Link"])
                match["Home_Player_Stats"] = home_player_stats
                match["Away_Player_Stats"] = away_player_stats
                match["Home_Goalie_Stats"] = home_goalie_stats
                match["Away_Goalie_Stats"] = away_goalie_stats
        return fixtures_dict
    
    def get_match_data(self, url: str) -> list:
        game_soup = self.get_page_soup(url)
        team_game_stats = game_soup.find_all(id=re.compile("all_player_stats"))
        goalie_game_stats = game_soup.find_all(id=re.compile("keeper_stats"), class_="table_wrapper")

        player_column_names = {
                            'Unnamed: 0_level_0_Player': 'player_name',
                            'Unnamed: 3_level_0_Pos': 'position',
                            'Unnamed: 5_level_0_Min': 'minutes_played',
                            'Performance_Gls': 'goals',
                            'Performance_Ast': 'assists',
                            'Performance_PK': 'penalties',
                            'Performance_Sh': 'shots',
                            'Performance_SoT': 'shots_on_target',
                            'Performance_Touches': 'touches',
                            'Performance_Tkl': 'tackles',
                            'Performance_Int': 'interceptions',
                            'Performance_Blocks': 'blocks',
                            'Expected_xG': 'xg',
                            'Expected_npxG': 'npxg',
                            'Expected_xAG': 'xag',
                            'SCA_SCA': 'sca',
                            'SCA_GCA': 'gca',
                            'Passes_Cmp': 'passes_completed',
                            'Passes_Att': 'passes_attempted',
                            'Passes_Cmp%': 'pass_accuracy',
                            'Passes_PrgP': 'progressive_passes',
                            'Carries_Carries': 'carries',
                            'Carries_PrgC': 'progressive_carries',
                            'Take-Ons_att':'take_ons_attempted',
                            'Take-Ons_Succ': 'take_ons_successful'
                            }
        goalie_column_names = {'Unnamed: 0_level_0_Player': 'player_name',
                             'Unnamed: 3_level_0_Min': 'minutes_played',
                             'Shot Stopping_SoTA': 'sota',
                             'Shot Stopping_GA': 'goals_allowed',
                             'Shot Stopping_Saves': 'saves',
                             'Shot Stopping_Save%': 'save_percentage',
                             'Shot Stopping_PSxG': 'psxg',
                             'Launched_Cmp': 'passes_completed',
                             'Launched_Att': 'passes_attempted',
                             'Launched_Cmp%': 'pass_accuracy',
                             'Passes_Att (GK)': 'gk_passes_attempted',
                             'Passes_Thr': 'throws',
                             'Passes_Launch%': 'launch_percentage',
                             'Passes_AvgLen': 'launch_average_length',
                             'Goal Kicks_Att': 'goal_kicks_attempted',
                             'Goal Kicks_Launch%': 'goal_kick_launch_percentage',
                             'Goal Kicks_AvgLen': 'goal_kick_average_length',
                             'Crosses_Opp': 'crosses_opportunities',
                             'Crosses_Stp': 'crosses_stops',
                             'Crosses_Stp%': 'crosses_stop_percentage',
                             'Sweeper_#OPA': 'opa',
                             'Sweeper_AvgDist': 'opa_average_distance'
                            }

        stats = []
        for team_stat in team_game_stats:
            team_stat_df = pd.read_html(io.StringIO(str(team_stat)))[0]
            team_stat_df.columns = ['_'.join(col).strip() for col in team_stat_df.columns.values]
            team_stat_df = team_stat_df.rename(columns=player_column_names)
            stats.append(team_stat_df.to_dict(orient='records'))
        for count, goalie_stat in enumerate(goalie_game_stats):
            goalie_stat_df = pd.read_html(io.StringIO(str(team_stat)))[0]
            goalie_stat_df.columns = ['_'.join(col).strip() for col in goalie_stat_df.columns.values]
            goalie_stat_df = goalie_stat_df.rename(columns=player_column_names)
            stats.append(goalie_stat_df.to_dict(orient='records'))
        print(len(stats))
        return stats
