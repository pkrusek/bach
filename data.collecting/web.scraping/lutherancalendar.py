from pprint import pprint
from datetime import datetime, timedelta
import enum
import helpers
import warnings
import pandas as pd

warnings.simplefilter(action='ignore', category=FutureWarning)


class EventType(enum.Enum):
    ADV1 = {'title': 'Advent I', 'link': 'https://en.wikipedia.org/wiki/Advent', 'bwv': [36, 61, 62]}
    # ADV2 = {'title': 'Advent II', 'link': 'https://en.wikipedia.org/wiki/Advent', 'bwv': []}
    # ADV3 = {'title': 'Advent III', 'link': 'https://en.wikipedia.org/wiki/Advent', 'bwv': []}
    ADV4 = {'title': 'Advent IV', 'link': 'https://en.wikipedia.org/wiki/Advent', 'bwv': [132]}
    CHR1 = {'title': 'Christmas Day', 'link': 'https://en.wikipedia.org/wiki/Christmas', 'bwv': [63, 91, 110, 191]}
    CHR2 = {'title': "Saint Stephen's Day", 'link': 'https://en.wikipedia.org/wiki/Saint_Stephen%27s_Day', 'bwv': [40, 57, 121]}
    CHR3 = {'title': 'Third day of Christmas', 'link': 'https://en.wikipedia.org/wiki/Christmas', 'bwv': [64, 133, 151]}
    CHR4 = {'title': 'Sunday after Christmas', 'link': 'https://en.wikipedia.org/wiki/Christmas_Sunday', 'bwv': [28, 122, 152]}
    NYD1 = {'title': "New Year's Day", 'link': 'https://en.wikipedia.org/wiki/New_Year%27s_Day', 'bwv': [16, 41, 143, 171, 190]}
    NYD2 = {'title': "New Year's Day I", 'link': 'https://en.wikipedia.org/wiki/New_Year%27s_Day', 'bwv': [58, 153]}
    EPH0 = {'title': "Epiphany", 'link': 'https://en.wikipedia.org/wiki/Epiphany_(holiday)', 'bwv': [65, 123]}
    EPH1 = {'title': "Epiphany I", 'link': 'https://en.wikipedia.org/wiki/Epiphany_(holiday)', 'bwv': [32, 124, 154]}
    EPH2 = {'title': "Epiphany II", 'link': 'https://en.wikipedia.org/wiki/Epiphany_(holiday)', 'bwv': [3, 13, 155]}
    EPH3 = {'title': "Epiphany III", 'link': 'https://en.wikipedia.org/wiki/Epiphany_(holiday)', 'bwv': [72, 73, 111, 156]}
    EPH4 = {'title': "Epiphany IV", 'link': 'https://en.wikipedia.org/wiki/Epiphany_(holiday)', 'bwv': [14, 81]}
    # EPH5 = {'title': "Epiphany V", 'link': 'https://en.wikipedia.org/wiki/Epiphany_(holiday)', 'bwv': []}
    SEPT = {'title': "Septuagesima", 'link': 'https://en.wikipedia.org/wiki/Septuagesima', 'bwv': [84, 92, 144]}
    SEXA = {'title': "Sexagesima", 'link': 'https://en.wikipedia.org/wiki/Sexagesima', 'bwv': [18, 126, 181]}
    ESTO = {'title': "Quinquagesima", 'link': 'https://en.wikipedia.org/wiki/Quinquagesima', 'bwv': [22, 23, 127, 159]}
    PALM = {'title': "Palm Sunday", 'link': 'https://en.wikipedia.org/wiki/Palm_Sunday', 'bwv': [182]}
    # GOOF = {'title': "Good Friday", 'link': 'https://en.wikipedia.org/wiki/Good_Friday', 'bwv': []} passion
    # HOLS = {'title': "Holy Saturday", 'link': 'https://en.wikipedia.org/wiki/Holy_Saturday', 'bwv': []}
    EAS1 = {'title': "Easter", 'link': 'https://en.wikipedia.org/wiki/Easter', 'bwv': [4, 31]}
    EAS2 = {'title': "Easter Monday", 'link': 'https://en.wikipedia.org/wiki/Easter', 'bwv': [6, 66]}
    EAS3 = {'title': "Easter Tuesday", 'link': 'https://en.wikipedia.org/wiki/Easter', 'bwv': []}


events = pd.DataFrame(columns=['Date', 'Event Type'])


def get_static_dates(year):
    # only events with cantata
    events.loc[len(events)] = [f'{year}-12-25', EventType.CHR1.name]
    events.loc[len(events)] = [f'{year}-12-26', EventType.CHR2.name]
    events.loc[len(events)] = [f'{year}-12-27', EventType.CHR3.name]
    events.loc[len(events)] = [f'{year}-01-01', EventType.NYD1.name]
    events.loc[len(events)] = [f'{year}-01-02', EventType.NYD2.name]
    events.loc[len(events)] = [f'{year}-01-06', EventType.EPH0.name]

    events["Date"] = pd.to_datetime(events["Date"])


def get_dynamic_dates(year):
    adv4 = helpers.get_last_weekday(helpers.get_date_from_str(f'{year}-12-25'), 6)
    adv3 = adv4 - timedelta(weeks=1)
    adv2 = adv4 - timedelta(weeks=2)
    adv1 = adv4 - timedelta(weeks=3)
    eas1 = helpers.get_easter(year)
    hols = helpers.get_last_weekday(eas1, 5)
    goof = helpers.get_last_weekday(eas1, 4)
    palm = eas1 - timedelta(weeks=1)
    esto = palm - timedelta(weeks=6)
    sexa = esto - timedelta(weeks=1)
    sept = sexa - timedelta(weeks=1)
    eas2 = eas1 + timedelta(days=1)
    eas3 = eas1 + timedelta(days=2)

    sunday_after_christmas = helpers.get_next_weekday(helpers.get_date_from_str(f'{year}-12-25'), 6)
    if sunday_after_christmas.year == year:
        events.loc[len(events)] = [sunday_after_christmas, EventType.CHR4.name]

    eph1 = helpers.get_next_weekday(helpers.get_date_from_str(f'{year}-01-06'), 6)

    for index, key in enumerate([EventType.EPH2.name, EventType.EPH3.name, EventType.EPH4.name]):
        date = eph1 + timedelta(weeks=index + 1)
        if date < sept:
            events.loc[len(events)] = [date, key]

    events.loc[len(events)] = [adv1, EventType.ADV1.name]
    # events.loc[len(events)] = [adv2, EventType.ADV2.name]
    # events.loc[len(events)] = [adv3, EventType.ADV3.name]
    events.loc[len(events)] = [adv4, EventType.ADV4.name]
    events.loc[len(events)] = [eas1, EventType.EAS1.name]
    # events.loc[len(events)] = [hols, EventType.HOLS.name]
    # events.loc[len(events)] = [goof, EventType.GOOF.name]
    events.loc[len(events)] = [palm, EventType.PALM.name]
    events.loc[len(events)] = [esto, EventType.ESTO.name]
    events.loc[len(events)] = [sexa, EventType.SEXA.name]
    events.loc[len(events)] = [sept, EventType.SEPT.name]
    events.loc[len(events)] = [eph1, EventType.EPH1.name]
    events.loc[len(events)] = [eas2, EventType.EAS2.name]
    events.loc[len(events)] = [eas3, EventType.EAS3.name]

    df = events.sort_values(by="Date")
    pprint(df)


if __name__ == '__main__':
    get_static_dates(2022)
    get_dynamic_dates(2022)
