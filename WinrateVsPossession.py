from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.ticker as mtick
from matplotlib.ticker import PercentFormatter
import matplotlib.pyplot as plt
import numpy as np
from selenium import webdriver
from datetime import datetime, date, time, timedelta
import os

teamsHashMap = {
                'denver broncos': 'den',
                'new england patriots':'nwe',
                'buffalo bills':'buf',
                'new york jets':'nyj',
                'miami dolphins':'mia',
                'baltimore ravens':'rav',
                'pittsburgh steelers':'pit',
                'clevland browns':'cle',
                'cincinatti bengals':'cin',
                'houston texans':'htx',
                'tennesse titans':'oti',
                'indianapolis colts':'clt',
                'jacksonville jaguars':'jax',
                'kansas city chiefs':'kan',
                'las vegas raiders':'rai',
                'los angeles chargers':'sdg',
                'philidelphia eagles':'phi',
                'dallas cowboys':'dal',
                'new york giants':'nyg',
                'washington redskins':'was',
                'greenbay packers':'gnb',
                'minnesota vikings':'min',
                'chicago bears':'chi',
                'detroit lions':'det',
                'new oreleans saints':'nor',
                'tampa bay buccaneers':'tam',
                'atlanta falcons':'atl',
                'carolina panthers':'car',
                'san fransisco 49ers':'sfo',
                'seatle seahawks':'sea',
                'los angeles rams':'ram',
                'arizona cardinals':'crd'
                }

ab_teamsHashMap = {
                'den':'DEN',
                'nwe':'NWE',
                'buf':'BUF',
                'nyj':'NYJ',
                'mia':'MIA',
                'rav':'BAL',
                'pit':'PIT',
                'cle':'CLE',
                'cin':'CIN',
                'htx':'HOU',
                'oti':'TEN',
                'clt':'IND',
                'jax':'JAX',
                'kan':'KAN',
                'rai':'OAK',
                'sdg':'LAC',
                'phi':'PHI',
                'dal':'DAL',
                'nyg':'NYG',
                'was':'WAS',
                'gnb':'GNB',
                'min':'MIN',
                'chi':'CHI',
                'det':'DET',
                'nor':'NOR',
                'tam':'TAM',
                'atl':'ATL',
                'car':'CAR',
                'sfo':'SFO',
                'sea':'SEA',
                'ram':'LAR',
                'crd':'ARI'
                }



class allgamestats():

    def __init__(self):
        None

    def get_df(self, team, year):  # Retrieves the CSV file and converts to a dataframe

        fpath = 'All_GamesDB/' + year + team + 'all_games.csv'

        df = pd.read_csv(fpath)
        df = df.iloc[:17]
        df = df['game_date'].loc[df['game_location'] != '@']

        df = df.to_frame()

        size, _ = df.shape
        tc = []
        for i in range(size):
            tc.append(team)
        df['Team'] = tc

        return df

    def compile_df(self):

        total_df = pd.DataFrame(None,None,columns=['Team', 'Date'])
        total_df = pd.DataFrame(total_df, index=[0])

        for team in teamsHashMap:
            appended_df = self.get_df(teamsHashMap[team], '2019')
            appended_df = appended_df.rename(columns={'game_date': 'Date'})
            total_df = total_df.append(appended_df, ignore_index=True, sort=True)

        total_df = total_df.set_index('Team')

        for index, row in total_df.iterrows():
            try:
                date = datetime.strptime(row['Date'], "%B %d")
                row['Date'] = date.strftime("2019%m%d")
            except:
                continue
        total_df = total_df.dropna()

        return total_df

    def get_page(self, team, date):

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
        driver.get('https://www.pro-football-reference.com/boxscores/' + date + '0' + team + '.htm')
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')
        
        return soup

    def get_team_stats(self, team, date):

        statHashMap = {}

        raw_table_data = self.get_page(team, date).find(id="div_team_stats")
        raw_table_data_list = raw_table_data.find_all('td')
        raw_table_data_list_2 = raw_table_data.find_all('th')

        for th in raw_table_data_list_2:
            if th.get("data-stat") not in statHashMap:
                statHashMap[th.get("data-stat")] = [th.get_text()]
            else:
                statHashMap[th.get("data-stat")].append(th.get_text())

        for td in raw_table_data_list:
            if td.get("data-stat") not in statHashMap:
                statHashMap[td.get("data-stat")] = [td.get_text()]
            else:
                statHashMap[td.get("data-stat")].append(td.get_text())

        df = pd.DataFrame.from_dict(statHashMap, orient='index')
        df = df.transpose()
        df.to_csv('GameStatsDB/' + date + team + '.csv', index=False)

        return df

    def set_all_team_stats(self):

        df = self.compile_df()
        count = 0
        for index, row in df.iterrows():
            try:
                self.get_team_stats(index, row['Date'])
            except:
                continue

        return None

class WinrateVsPossession():

    def __init__(self):
        self.possessionHash = {}
        self.winrateHash = {}

    def set_possession(self):

        for fpath in os.listdir('GameStatsDB/'):
            df = pd.read_csv('GameStatsDB/' + fpath)

            if df.loc[0, 'home_stat'] in self.possessionHash:
                self.possessionHash[df.loc[0, 'home_stat']].append(df.loc[12, 'home_stat'])
            else:
                self.possessionHash[df.loc[0, 'home_stat']] = [df.loc[12, 'home_stat']]

            if df.loc[0, 'vis_stat'] in self.possessionHash:
                self.possessionHash[df.loc[0, 'vis_stat']].append(df.loc[12, 'vis_stat'])
            else:
                self.possessionHash[df.loc[0, 'vis_stat']] = [df.loc[12, 'vis_stat']]

        return None

    def get_avg_possession(self):

        df = pd.DataFrame.from_dict(self.possessionHash)
        avg_possession_map = {}

        for label, content in df.items():
            avg = 0
            count = 0
            for possession in content:
                count+=1
                current_possession = datetime.strptime(possession, '%M:%S').time()
                current_possession = current_possession.second + current_possession.minute*60 + current_possession.hour*3600
                avg += current_possession

            avg = avg/(count*60)

            avg_possession_map[label] = avg

        return avg_possession_map

    def get_winrate(self):

        for team in teamsHashMap:

            fpath = 'All_GamesDB/2019' + teamsHashMap[team] + 'all_games.csv'

            df = pd.read_csv(fpath)
            df = df.iloc[:17]
            wins = df[df.game_outcome == 'W'].shape[0]
            losses = df[df.game_outcome == 'L'].shape[0]
            ties = df[df.game_outcome == 'T'].shape[0]

            winrate = (wins + (.5)*ties)/(wins+losses+ties)

            self.winrateHash[ab_teamsHashMap[teamsHashMap[team]]] = float(winrate)

        return self.winrateHash

wr = WinrateVsPossession()
wr.set_possession()
d1 = wr.get_winrate()
d2 = wr.get_avg_possession()

ds = [d1, d2]
d = {}
for k in d1.keys():
  d[k] = tuple(d[k] for d in ds)

d = pd.DataFrame.from_dict(d)
d = d.rename(index={0: "winrate", 1: "possession"}).T


y = np.array(d['winrate']*100)
x = np.array(d['possession'])


m, b = np.polyfit(x, y, 1)

plt.scatter(x, y, marker = 'o')
ax = plt.gca()
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
plt.plot(x, m*x + b, color = 'red')
plt.gcf().autofmt_xdate()

plt.xlabel('Possession (minutes)')
plt.ylabel('Winrate ((Wins + .5*Ties)/Total)')
plt.grid(True,)
plt.title('Possession versus Winrate')

plt.show()
