import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd
from tabulate import tabulate as tab

# request
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}
URL = 'https://de.wikipedia.org/wiki/Liste_der_Bachkantaten'
page = req.get(URL, headers=headers)

# soup
soup = bs(page.content, 'html.parser')
all_cantatas = soup.find_all('table', class_='wikitable sortable')[0]

# pandas
df = pd.read_html(str(all_cantatas))[0]
res = df.loc[:, ['BWV', 'Titel']]
res.to_csv("../_data/cantatas.csv", header=False, index=False)
