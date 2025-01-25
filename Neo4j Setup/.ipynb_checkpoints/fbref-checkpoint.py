import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import pickle
import re
from IPython.display import clear_output
import io

class FBRef:
    def __init__(self):
        self.fbref_url = "https://fbref.com{}"

    def make_request(self, endpoint: str) -> str:
        while True:
            response = requests.get(endpoint)
            if response.status_code == 429:  # Rate limited
                print("Rate limited. Pausing for 5 minutes...")
                print(endpoint)
                print(response.text)
                time.sleep(300)  # Wait for 5 minutes
            else:
                return response.text

    def get_page_soup(self, url: str) -> BeautifulSoup:
        return BeautifulSoup(self.make_request(url), 'html.parser')

    def extract_team_links(self, url: str) -> dict:
        league_teams_soup = self.get_page_soup(url)
        league_table = league_teams_soup.select('table.stats_table')[0]
        teams_dict = {
            team_link.get_text(): self.fbref_url.format(team_link.get("href"))
            for team_link in league_table.find_all('a') if "squads" in team_link.get("href")
        }
        return teams_dict

    def extract_player_links(self, url: str) -> dict:
        team_soup = self.get_page_soup(url)
        team_players_table = team_soup.select('table.stats_table')[0]
        players_links_dict = {
            l.get_text(): self.fbref_url.format(l.get("href"))
            for l in team_players_table.find_all('a')
            if (link := l.get("href")) and "players" in link and "matchlogs" not in link
        }
        return players_links_dict

    def extract_player_details(self, url: str) -> dict:
        player_soup = self.get_page_soup(url)
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

    def get_fixtures(self, url: str) -> BeautifulSoup:
        fixtures_soup = self.get_page_soup(url)
        fixtures_table = fixtures_soup.find(id='all_sched')
        return fixtures_table

    def get_match_data(self, url: str) -> list:
        game_soup = self.get_page_soup(url)
        team_stats = list()
        team_game_stats = game_soup.find_all(id=re.compile("all_player_stats"))
        goaly_game_stats = game_soup.find_all(id=re.compile("keeper_stats"), class_="table_wrapper")
        for team_stat in team_game_stats:
            team_stats.append(pd.read_html(str(team_stat))[0])
        for count, goaly_stat in enumerate(goaly_game_stats):
            goaly_df = pd.read_html(str(goaly_stat))[0]
            team_stats[count] = [team_stats[count], goaly_df]
        return team_stats
