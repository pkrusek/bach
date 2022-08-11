import pandas as pd

import helpers
from pprint import pprint


def get_calendar_2021_2022():
    sp = helpers.make_request('https://whichbachcantata.be/bach-cantata-calendars-2020-to-2037.html')
    sp_lis = sp.find_all('ul')[2].findChildren('li')
    data = list(map(lambda li: li.text, sp_lis))
    df = pd.DataFrame(data)
    df.to_csv("./_data/calendar-21-22.csv", header=False, index=False)


if __name__ == '__main__':
    get_calendar_2021_2022()
