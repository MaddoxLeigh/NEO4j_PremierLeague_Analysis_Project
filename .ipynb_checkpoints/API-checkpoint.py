import requests
import json
import pandas as pd
import time


# https://www.football-data.org/documentation/quickstart
football_data_api = 'https://api.football-data.org/v4/'
football_data_token = 'b23230b1dbb646fc9e4c5e38cd2f046f'


r = requests.get(
    football_data_api + 'competitions/PL/teams',
    headers={'X-Auth-Token': football_data_token}
)

data = json.loads(r.text)

for team in data['teams']:
    team['area'] = team['area']['id']
    team['runningCompetitions'] = [competition['id'] for competition in team['runningCompetitions']]
    team['squad'] = [player['id'] for player in team['squad']]
    team['coach'] = team['coach']['id']

df_teams = pd.DataFrame(data['teams'])
squad = sum(df_teams['squad'],[])

squad_details = dict()

for count, squad_id in enumerate(squad,start=1):
    print(f"Currently at player {count}. Progress: {(count/len(squad))*100}")
    r = requests.get(
    football_data_api + f'persons/{squad_id}',
    headers={'X-Auth-Token': football_data_token})
    data = json.loads(r.text)
    squad_details[squad_id] = data
    if count % 10 == 0 and count != 0 and count != len(squad):
        time.sleep(60)

        df_squad_details = pd.DataFrame.from_dict(squad_details, orient='index')
        df_squad_details.to_csv(f'squad_details{count}.csv', index=False)
        
df_squad_details = pd.DataFrame.from_dict(squad_details, orient='index')
df_squad_details.to_csv(f'squad_details{count}.csv', index=False)