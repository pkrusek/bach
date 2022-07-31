import requests as req
from bs4 import BeautifulSoup as bs


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}
URL = "https://www.bach-cantatas.com/IndexBWV1.htm"
page = req.get(URL, headers=headers)
