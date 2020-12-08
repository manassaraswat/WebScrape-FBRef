from bs4 import BeautifulSoup as soup
import requests
import re

squad = []
name = []
my_url = 'https://fbref.com/en/comps/20/1634/2017-2018-Bundesliga-Stats'

### Parse HTML from URL and get Player Data and Columns into Variables

res = requests.get(my_url)
comm = re.compile("<!--|-->")
page_soup = soup(comm.sub("", res.text), "html.parser")

containers = page_soup.findAll("div", {"id": "div_results16341_overall"})

container = containers[0]
teams_league = container.findAll('tr')

for row in teams_league:
    if row.find('th', {"scope": "row"}) is not None:
        name = row.a['href']
        squad.append(name)


print(len(squad))