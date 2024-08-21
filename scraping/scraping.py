'''
For one player:
Print goals for one game
print goals, assists, tka for one game
print all that stuff for each game in a month
print all that stuff for each game in a year
'''

# To run this, download the BeautifulSoup zip file
# http://www.py4e.com/code3/bs4.zip
# and unzip it in the same directory as this file

from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://www.statmuse.com/nhl/player/evgeni-malkin-4266/game-log'

# open html file
html = urlopen(url, context=ctx).read()
# get our soup object
soup = BeautifulSoup(html, "html.parser")

list_of_tables = soup.select('astro-island h3')
# print(list_of_tables[0].string)

for table in list_of_tables:
  print(table.string)


list_of_dates = soup.select('astro-island')

