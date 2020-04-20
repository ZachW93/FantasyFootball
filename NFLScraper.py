from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pylab as plt
import tkinter as tk
from selenium import webdriver

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

stats = {
    'rushing passing': 'all_rushing_and_receiving',
    'returns':'all_returns',
    'kicking':'all_kicking',
    'defense':'all_defense',
    'total td':'all_scoring',
    'td log':'all_team_td_log',
    'opponent td':'all_opp_td_log'
    }

#teamName = teamsHashMap[input("Please select a Team to view: ").lower()]
#year = input("Please Enter the Year: ")

class teamstats():
    
    def __init__(self, team, year):
        self.team = str(team)
        self.year = str(year)
    
    
    def get_page(self):
        
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
        driver.get('https://www.pro-football-reference.com/teams/' + self.team + '/' + self.year + '.htm')
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')

        return soup
    
    def get_stats(self):
        statHashMap = {}
        for key in stats:
            print(key)
            
        desiredstat = input("Please select a stat to view: ")
        
        raw_table_data = self.get_page().find(id=stats[desiredstat.lower()]) #Finding the table in the HTML code for the previous URL
        raw_table_data_list = raw_table_data.find_all('td')
        for td in raw_table_data_list:
            if td.get("data-stat") not in statHashMap:
                statHashMap[td.get("data-stat")] = [td.get_text()]
            else:
                statHashMap[td.get("data-stat")].append(td.get_text())
        
        df = pd.DataFrame.from_dict(statHashMap, orient='index')
        
        df.to_csv(r'C:\Users\Zach\Desktop\github\FantasyFootball\export_dataframe.csv', index=True)

root = tk.Tk()
root.title("Tk dropdown example")

# Add a grid
mainframe = tk.Frame(root)
#mainframe.grid(column=0,row=0, sticky=(N,W,E,S))
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 100, padx = 100)

# Create a Tkinter variable
tkvar = tk.StringVar(root)

# Dictionary with options
choices = {
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
tkvar.set('') # set the default option

popupMenu = tk.OptionMenu(mainframe, tkvar, *choices)
tk.Label(mainframe, text="Please Select a Team: ").grid(row = 1, column = 1)
popupMenu.grid(row = 2, column =1)

# on change dropdown value
def change_dropdown(*args):
    print( tkvar.get() )

# link function to change dropdown
tkvar.trace('w', change_dropdown)

root.mainloop()
    
#teamstats = teamstats(teamName, year)
#print(teamstats.get_stats())