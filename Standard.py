from bs4 import BeautifulSoup as soup
import requests
import re
import pandas as pd
import ScrapperMain



my_url = "https://fbref.com/en/comps/Big5/stats/players/Big-5-European-Leagues-Stats"
string = my_url.split('/', int(my_url.find('/')) + 2)
column_names = []
player_names = []
players_data = []

### Parse HTML from URL and get Player Data and Columns into Variables
res = requests.get(my_url)
comm = re.compile("<!--|-->")
page_soup = soup(comm.sub("", res.text), "html.parser")

containers = page_soup.findAll("div", {"id": "div_stats_standard"})
#print(page_soup.prettify(containers[0]))
# print(len(containers))
container = containers[0]
stat = container.findAll('th')
numbers = container.findAll('td')

### Map Data in Variables into Lists
for a in range(7, 38):
    column_names.append(stat[a].text)

for a in range(38, len(stat)):
    player_names.append(stat[a].text)

for a in range(0, len(numbers)):
    players_data.append(numbers[a].text)

###Create a list of lists for Player Data
players_data2 = [players_data[a:a + (len(column_names) - 1)] for a in
                 range(0, len(numbers), (len(column_names) - 1))]

###Mapping All Data into DataFrames
df = pd.DataFrame(columns=column_names)
df['Player'] = player_names

df2 = pd.DataFrame(players_data2)
df2.insert(0, df.columns[0], df['Player'])

df3 = pd.DataFrame(df2.values, columns=df.columns)

###Export to Excel
df3.to_excel("StandardStats" + string[6] + ".xlsx", index=False)

df.empty
df2.empty
df3.empty

