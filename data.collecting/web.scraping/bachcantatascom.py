import pandas as pd
import requests as req
from bs4 import BeautifulSoup as bs
from pprint import pprint

import helpers


def get_main_table():
    sp = helpers.make_request('https://www.bach-cantatas.com/BWV1.htm')
    sp_table = sp.find_all('table', {'bordercolor': '#0000ff'})[0]
    df = pd.read_html(str(sp_table))[0]
    df.to_csv("./_data/test.csv", index=False)
    return df

# class BachCantatasCom:
#
#     @staticmethod
#     def get_main_table():
#         # self.is_not_used()
#         sp = helpers.make_request('https://www.bach-cantatas.com/BWV1.htm')
#         sp_table = sp.find_all('table', {'bordercolor': '#0000ff'})[0]
#         df = pd.read_html(str(sp_table))[0]
#
#         return df
#
#     def is_not_used(self):
#         pass
