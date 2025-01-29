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
    """
    Class for reading in our data files from within the data directory. These are JSON files.
    """
    

    def __init__(self, data_directory):
        """
        Classa initiator function
        data_directory: file path to the data directory for which all the files are located in.
        """
        self.data_directory = data_directory

    def load_data(self, data, season):
        """
        Function to read in the necessary data.
        data: the file name for which the data is located in
        season: the season of this particular data.

        Season is necessary as all data is seperated by folders of season.
        """
        file_path = os.path.join(self.data_directory, season, f"{data}.json")
        with open(file_path, "r") as f:
            return json.load(f)
    
    def listdir(self, directory:str) -> list:
        """
        Function to list all files within a directory, but not include the hidden files which start with '.'
        """
        return [x for x in os.listdir(os.path.join(self.data_directory, directory)) if x[0] != '.']

class FBRefDataWriter:
    """
    Class for writing data to within our data directory. These are all written to JSON files.
    """

    def __init__(self, data_directory):
        """
        Class initiator function to set the data directory'
        """
        self.data_directory = data_directory

    def write_data(self, data, season, file_name):
        """
        Function to write JSON data with to a season directory.
        data: the data to write to disk
        season: the season for which this data relates to (and therefore the directory which it needs to be saved to)
        file_name: the name for the file to be written.
        """
        file_path = os.path.join(self.data_directory, season, f"{file_name}.json")
        with open(file_path, "w") as f:
            return json.dump(data, f)


class FBRefDataFormatter:
    """
    Class for formatting data used in any notebook
    """

    def __init__(self):
        self.a = True

    def add_team_name_to_player(self, player_details, team_details):
        """
        As the team of a player might be different to that on their player page, we need to add the team that they played in that season into  their player details dictionary. 

        We do this by itearting over the team_details which contains a list of players for each team and we write the team name, the team they played for in a given season, to the player dictionary.

        We also add their name to within this dictionary (in a way flatten the player details dictionary to a player_name:player_details format to just a dictionary) and returning these dictionaries as a list.
        """
        
        for team_name, players_names_list in team_details.items():
            for player in players_names_list:
                if player in player_details.keys():
                    player_details[player]['Team'] = team_name
        for player in player_details.keys():
            player_details[player]['Name'] = player
        player_details = list(player_details.values())
        return player_details

    def split_match_data(self, match_report):
        """
        Function to split the match data json into 3 lists. 
        match_report: json file (interpreted as a dict)
        """

    

        #  match_data_list: list of dictionaries which represent general match statistics (Venue, Referee, Time, Gameweek etc)
        # player_stats_list: list of dictionaries for each players performance
        # goalie_stats_list list of dictionaries for each goalies performance 
        match_data_list = [] 
        player_stats_list = [] 
        goalie_stats_list = []  


        # for every match within this file
        for match in match_report:
            # extract the match id
            match_id = match["Match_ID"]

            # extract the general match data, not player specific
            match_data = {k: v for k, v in match.items() if k not in ["Home_Player_Stats", "Away_Player_Stats", "Home_Goalie_Stats", "Away_Goalie_Stats"]}
            # aadd this to the match data list 
            match_data_list.append(match_data)
    
            # retrieve the home and away player statistics
            home_player_stats = match["Home_Player_Stats"]
            away_player_stats = match["Away_Player_Stats"]

            # for each individual player statistic within the combination of these two lists
            for player in home_player_stats + away_player_stats:

                # add the match_id to their statistics dictionary, as well as their team name for this game
                player["match_id"] = match_id  
                player["team_name"] = match_data["Home"] if player in home_player_stats else match_data["Away"]
                player_stats_list.append(player)
                
            # do the same for goalies
            home_goalie_stats = match["Home_Goalie_Stats"]
            away_goalie_stats = match["Away_Goalie_Stats"]
            for goalie in home_goalie_stats + away_goalie_stats:
                goalie["match_id"] = match_id  
                goalie["team_name"] = match_data["Home"] if player in home_player_stats else match_data["Away"]
                goalie_stats_list.append(goalie)
    
        return match_data_list, player_stats_list, goalie_stats_list

class FBRefExtractor:
    """
    Class for extracting specific data from the FBRef website.
    """
    
    def __init__(self, season):
        """
        class initiator function.

        season: string of the season for which we are extracting data for
        """
        self.fbref_url = "https://fbref.com{}"
        # this will be a list of all requests made in any past minute. this is to prevent being rate limited by the website
        self.request_timestamps = list()
        self.set_season(season)

    def set_season(self, season):
        """
        To set the season for which we are extracting data for.
        season: yyyy-yyyy string of the season.
        """
        self.season = season
        # we need to check if this year is the current season as the endpoints are structured differently if so
        self.is_current_season = self.check_current_season()

    def check_current_season(self):
        # extract the start and end year from teh string
        start_year, end_year = map(int, self.season.split("-"))
        
        today = datetime.today()

        # as seasons start first week of august, and end last week of may we can use this logic to determine if we are in the current season.
        season_start = datetime(start_year, 8, 1)
        season_end = datetime(end_year, 5, 31)   

        return season_start <= today <= season_end

    def enforce_rate_limit(self):
        """
        Function to ensure we do not get rate limiting by allowing at most 16 requests per minute.
        """
        now = time.time()
        # we wait random time between 3 and 4 seconds to make each request as if it was a precise amount of time, we waited between requests we would have been detected as a bot
        time.sleep(random.uniform(3,4))
        # filter our request_timestamps list into only the timestamps that have occured within the last minute
        self.request_timestamps = [ts for ts in self.request_timestamps if now - ts <= 60]

        # if we have made at least 16 requests in the past minute wait until that decreases to 15
        if len(self.request_timestamps) >= 16:
            wait_time = 60 - (now - self.request_timestamps[0])
            print(f"Waiting: {wait_time}")
            time.sleep(wait_time)
        # as this funciton is only called by the make_requerst function, we know that it will be making a request immediately after this. so add our current time stamp to the list that stores request timestamps
        self.request_timestamps.append(time.time())

    def construct_season_stats_endpoint(self):
        """
        Construcut the endpoint for the specified seasons statistics page. This is an addition to the general season page
        """
        endpoint_stem = self.construct_season_endpoint()
        return endpoint_stem+"Premier-League-Stats"
    
    def construct_season_fixtures_endpoint(self):
        """
        Construct the endpoint for the sepcified seasons fixtures page. 
        """
        endpoint_stem = self.construct_season_endpoint()
        return endpoint_stem+"-Scores-and-Fixtures"
        
    def construct_season_endpoint(self, **kwargs):
        """
        Construct the general endpoint for this season

        current season endpoint looks as follow: /en/comps/9/Premier-League
        historical season endpoint look sas follow (2023 for example): /en/comps/9/2023-2024/2023-2024-Premier-League
        """

        # fixture endpoints are an exception and dont just stem on from the general endpoint, so we need to add this case where we include fixtures before the stats path.
        fixtures_path = "schedule" if kwargs.get("id") == "fixtures" else ""

        # construction depending on if we are in the current season
        season_path = self.season if not self.is_current_season else ""
        stats_path = (self.season+"-" if not self.is_current_season else "")
        return f"/en/comps/9/{season_path}/{fixtures_path}/{stats_path}Premier-League"
                
    def make_request(self, endpoint: str) -> str:
        """
        Function to make requests to the fbref website from. This constructs the full url from the endpoint
        """
        # call the rate enforcer
        self.enforce_rate_limit()
        # construct full url
        url = self.fbref_url.format(endpoint)
        # while we haven't been rate limited
        while True:
            # try to make the request
            response = requests.get(url)
            # if we are rate limited wait 5 minutes (time set by the website) before making the next request
            if response.status_code == 429:
                print("Rate limited. Pausing for 5 minutes...")
                time.sleep(300)  
            # otherwise return the response text
            else:
                return response.text

    def get_page_soup(self, endpoint: str) -> BeautifulSoup:
        """
        Function to return the beautiful soup version of a page
        """
        # we simply make the request to the endpoint, and parse the response text to BeautifulSoup. 
        return BeautifulSoup(self.make_request(endpoint), 'html.parser')

    def extract_team_links(self, season_endpoint: str) -> dict:
        league_teams_soup = self.get_page_soup(season_endpoint)
        league_table = league_teams_soup.select('table.stats_table')[0]
        teams_dict = {
            team_link.get_text(): team_link.get("href")
            for team_link in league_table.find_all('a') if "squads" in team_link.get("href")
        }
        return teams_dict

    def extract_player_links(self, team_endpoint: str) -> dict:
        """
        Function to extract links to all player details pages from the team page.
        team_endpoint: endpoint for the team, respective to the season.
        """
        # first get the soup of the teams page
        team_soup = self.get_page_soup(team_endpoint)
        # extract the first table on the page, as this is the players table
        team_players_table = team_soup.select('table.stats_table')[0]
        # formulate a dictionary where the key is the players name and their value is their endpoint
        players_links_dict = {
            l.get_text(): l.get("href")
            for l in team_players_table.find_all('a')
            if (link := l.get("href")) and "players" in link and "matchlogs" not in link
        }
        return players_links_dict

    def extract_player_details(self, player_endpoint: str) -> dict:
        """
        Function to extract the details of a player from their player details page

        player_endpoitn: str the endpoint
        """

        # retrieve the soup of their page
        player_soup = self.get_page_soup(player_endpoint)
        # extract their image, if one
        media_item_div = player_soup.select_one('div.media-item')
        image_src = media_item_div.find('img')['src'] if media_item_div else None

        # initalise their data dictionary
        player_data = dict()

        # for each paragraph box on their page, we will try and extract the following details, if on their page at all
        for p in player_soup.find_all('p'):
            text = p.get_text(strip=True)
            # the position of which they play
            if "Position:" in text:
                # general formatting to extract said attribute
                position_part = text.split("▪")[0].strip()
                footed_part = text.split("▪")[1].strip() if "▪" in text else None
                player_data['position'] = position_part.split(":")[1].strip()
                if footed_part:
                    player_data['footed'] = footed_part.split(":")[1].strip()
            # their height and weight
            if "cm" in text and "kg" in text:
                height, weight = map(str.strip, text.split(',')[:2])
                player_data['height'] = height
                player_data['weight'] = weight.split('(')[0]
            # date of birth, and their place of birth if included
            if "Born:" in text:
                birth_data = p.find("span", {"data-birth": True})
                if birth_data:
                    player_data['dob'] = birth_data["data-birth"]
                    birth_place = birth_data.find_next_sibling("span")
                    if birth_place:
                        player_data['birth_place'] = birth_place.get_text(strip=True)[3:]  
            # national team
            if "National Team:" in text:
                player_data['national_team'] = text.split(":")[1].strip()
            # club
            if "Club:" in text:
                player_data['club'] = text.split(":")[1].strip()
            # wages and contract expiry
            if "Wages" in text:
                wages = p.select_one('.important').get_text(strip=True) if p.select_one('.important') else None
                player_data['wages'] = wages
                if "Expires" in text:
                    contract_expires = text.split("Expires")[1].split(".")[0].strip()
                    player_data['contract_expiry'] = contract_expires
        # if we have their image add this to the player data dictionary before returning
        if image_src:
            player_data['img'] = image_src
        return player_data

    def get_fixtures(self) -> BeautifulSoup:
        """
        Retrieve data from fixtures page
        """
        # first construct the endpoint, using the keyword argument id="fixtures" as this is an exception in general endpoint construction
        fixtures_endpoint = self.construct_season_endpoint(id="fixtures")
        # get the page soup
        fixtures_soup = self.get_page_soup(fixtures_endpoint)
        # extract the schedule/fixtures table
        fixtures_table = fixtures_soup.find(id='all_sched')
        # return the html
        return fixtures_table

    def fixtures_to_dict(self, fixtures):
        """
        Convert the html of the fixtures table to a dictionary, with some formatting.

        fixtures: html
        """
        
        # convert the html of the table to a pandas dataframe for easier manipulation
        fixtures_df = pd.read_html(io.StringIO(str(fixtures)))[0]

        # remove empty rows
        fixtures_df = fixtures_df[fixtures_df['Wk'].notna()].reset_index(drop=True)
        # split score into individual columns
        fixtures_df[['Home_Score', 'Away_Score']] = fixtures_df['Score'].str.split('–', expand=True)
        # format weeks into game weeks
        fixtures_df['Wk'] = "GW" + fixtures_df['Wk'].astype(int).astype(str)

        # rename some columns for better understanding
        fixtures_df = fixtures_df.rename(columns={'Wk':'GW', 'xG':"Home_Expected", 'xG.1':"Away_Expected", "Match Report":"Match_Report"})

        # extract the individual match report links per match(row) on the fixtures table
        match_report_links = [l.get('href') for l in fixtures.find_all('a') if "Match Report" in l]
        # in the case when this is the current season, not necessarily all matches will  have a report (as they are in the fixture) so pad this list so it can be added to the dataframe as a column regardless.
        if self.is_current_season:
            match_report_links.extend([None]*(len(fixtures_df)-len(match_report_links)))

        # more formatting
        fixtures_df["Match Report Link"] = match_report_links
        fixtures_df["Match_ID"] = f"{self.season}"+fixtures_df["GW"]+fixtures_df["Home"]+fixtures_df["Away"]
        fixtures_df["Match_Report"] = (fixtures_df["Match_Report"] == "Match Report")
        fixtures_df = fixtures_df.replace({np.nan: None})

        # convert the dataframe to a dictionary
        fixtures_dict = fixtures_df.to_dict(orient='records')
        return fixtures_dict

    def append_match_data(self, fixtures_dict):

        """
        Function to add individual match statistics to the fixtures dictionary which contains general statistics.
        """
        for count, match in enumerate(fixtures_dict):
            if match["Match_Report"]:
                home_player_stats, away_player_stats, home_goalie_stats, away_goalie_stats = self.get_match_data(match["Match Report Link"])
                match["Home_Player_Stats"] = home_player_stats
                match["Away_Player_Stats"] = away_player_stats
                match["Home_Goalie_Stats"] = home_goalie_stats
                match["Away_Goalie_Stats"] = away_goalie_stats
        return fixtures_dict
    
    def get_match_data(self, endpoint: str) -> list:
        """
        Function to retrieve match statistics for an individual game

        endpoint: the endpoint for the match report

        return: list of four elements: [home team player stats, away team player stats, home team goalie stats, away team goalie stats]
        """

        # get the soup of the page
        game_soup = self.get_page_soup(url)
        # find the table outlining both the player and goalie stats
        team_game_stats = game_soup.find_all(id=re.compile("all_player_stats"))
        goalie_game_stats = game_soup.find_all(id=re.compile("keeper_stats"), class_="table_wrapper")

        # dictionaries for renaming the columns
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

        # for each of the team stats and goalie stats format them and rename their columns. then convert them to dictionaries
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
        return stats
