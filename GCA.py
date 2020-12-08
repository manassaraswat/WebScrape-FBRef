from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import requests
import pandas as pd
import re

column_names = []
player_names = []
players_data = []
my_url = 'https://fbref.com/en/comps/Big5/2019-2020/gca/players/2019-2020-Big-5-European-Leagues-Stats'
string = my_url.split('/', int(my_url.find('/'))+2)


### Parse HTML from URL and get Player Data and Columns into Variables

res = requests.get(my_url)
comm = re.compile("<!--|-->")
page_soup = soup(comm.sub("", res.text), "html.parser")

containers = page_soup.findAll("div", {"id": "all_stats_gca"})
container = containers[0]
#print(soup.prettify(container))
stat = container.findAll('th')

numbers = container.findAll('td')

### Map Data in Variables into Lists
for i in range(7, 32):
    column_names.append(stat[i].text)
#print(column_names)
for i in range(32, len(stat)):
    player_names.append(stat[i].text)

for i in range(0, len(numbers)):
    players_data.append(numbers[i].text)

###Create a list of lists for Player Data
players_data2 = [players_data[i:i + (len(column_names)-1)] for i in range(0, len(numbers), (len(column_names)-1))]

###Mapping All Data into DataFrames
df = pd.DataFrame(columns=column_names)
df['Player'] = player_names

df2 = pd.DataFrame(players_data2)
df2.insert(0, df.columns[0], df['Player'])

df3 = pd.DataFrame(df2.values, columns=df.columns)


###Export to Excel
df3.to_excel("GCA" + string[6] + ".xlsx", index=False)



