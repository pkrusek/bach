from pprint import pprint
from datetime import datetime, timedelta
import enum
import helpers
import warnings
import pandas as pd
import re

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
    PURI = {'title': "Candlemas", 'link': 'https://en.wikipedia.org/wiki/Candlemas', 'bwv': [82, 83, 125]}
    SEPT = {'title': "Septuagesima", 'link': 'https://en.wikipedia.org/wiki/Septuagesima', 'bwv': [84, 92, 144]}
    SEXA = {'title': "Sexagesima", 'link': 'https://en.wikipedia.org/wiki/Sexagesima', 'bwv': [18, 126, 181]}
    ESTO = {'title': "Quinquagesima", 'link': 'https://en.wikipedia.org/wiki/Quinquagesima', 'bwv': [22, 23, 127, 159]}
    PALM = {'title': "Palm Sunday", 'link': 'https://en.wikipedia.org/wiki/Palm_Sunday', 'bwv': [182]}
    # GOOF = {'title': "Good Friday", 'link': 'https://en.wikipedia.org/wiki/Good_Friday', 'bwv': []} passion
    # HOLS = {'title': "Holy Saturday", 'link': 'https://en.wikipedia.org/wiki/Holy_Saturday', 'bwv': []}
    EAS1 = {'title': "Easter", 'link': 'https://en.wikipedia.org/wiki/Easter', 'bwv': [4, 31]}
    EAS2 = {'title': "Easter Monday", 'link': 'https://en.wikipedia.org/wiki/Easter', 'bwv': [6, 66]}
    EAS3 = {'title': "Easter Tuesday", 'link': 'https://en.wikipedia.org/wiki/Easter', 'bwv': [134, 145, 158]}
    QUAS = {'title': "Second Sunday of Easter (Quasimodogeniti)", 'link': 'https://en.wikipedia.org/wiki/Second_Sunday_of_Easter', 'bwv': [42, 67]}
    MISE = {'title': "Third Sunday of Easter (Misericordias Domini)", 'link': 'https://en.wikipedia.org/wiki/Third_Sunday_of_Easter', 'bwv': [85, 104, 112]}
    JUBI = {'title': "Fourth Sunday of Easter (Jubilate)", 'link': 'https://en.wikipedia.org/wiki/Fourth_Sunday_of_Easter', 'bwv': [12, 103, 146]}
    CANT = {'title': "Fifth Sunday of Easter (Cantate)", 'link': 'https://en.wikipedia.org/wiki/Fifth_Sunday_of_Easter', 'bwv': [108, 166]}
    ROGA = {'title': "Sixth Sunday of Easter (Rogate)", 'link': 'https://en.wikipedia.org/wiki/Rogation_days', 'bwv': [86, 87]}
    ASCE = {'title': "Holy Thursday (Ascension)", 'link': 'https://en.wikipedia.org/wiki/Feast_of_the_Ascension', 'bwv': [11, 37, 43, 128]}
    EXAU = {'title': "Sunday after the Ascension (Exaudi)", 'link': 'https://www.csmedia1.com/ziondetroit.org/exaudi.pdf', 'bwv': [44, 183]}
    ANNU = {'title': "Annunciation", 'link': 'https://en.wikipedia.org/wiki/Annunciation', 'bwv': [1]}
    WHI1 = {'title': "Whit Sunday (Pentecost)", 'link': 'https://en.wikipedia.org/wiki/Pentecost', 'bwv': [34, 59, 74, 172]}
    WHI2 = {'title': "Whit Monday", 'link': 'https://en.wikipedia.org/wiki/Whit_Monday', 'bwv': [68, 173, 174]}
    WHI3 = {'title': "Whit Tuesday", 'link': 'https://en.wikipedia.org/wiki/Whit_Tuesday', 'bwv': [175, 184]}
    TR00 = {'title': "Trinity", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [129, 165, 176, 194]}
    TR01 = {'title': "Trinity I", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [20, 39, 75]}
    TR02 = {'title': "Trinity II", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [2, 76]}
    TR03 = {'title': "Trinity III", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [21, 135]}
    TR04 = {'title': "Trinity IV", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [24, 177, 185]}
    TR05 = {'title': "Trinity V", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [88, 93]}
    TR06 = {'title': "Trinity VI", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [9, 170]}
    TR07 = {'title': "Trinity VII", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [54, 107, 186, 187]}
    TR08 = {'title': "Trinity VIII", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [45, 136, 178]}
    TR09 = {'title': "Trinity IX", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [94, 105, 168]}
    TR10 = {'title': "Trinity X", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [46, 101, 102]}
    TR11 = {'title': "Trinity XI", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [113, 179, 199]}
    TR12 = {'title': "Trinity XII", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [35, 137]}
    TR13 = {'title': "Trinity XIII", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [33, 77, 164]}
    TR14 = {'title': "Trinity XIV", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [17, 25, 78]}
    TR15 = {'title': "Trinity XV", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [51, 99, 138]}
    TR16 = {'title': "Trinity XVI", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [8, 27, 95, 161]}
    TR17 = {'title': "Trinity XVII", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [47, 114, 148]}
    TR18 = {'title': "Trinity XVIII", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [96, 169]}
    TR19 = {'title': "Trinity XIX", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [5, 48, 56]}
    TR20 = {'title': "Trinity XX", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [49, 162, 180]}
    TR21 = {'title': "Trinity XXI", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [38, 98, 109, 188]}
    TR22 = {'title': "Trinity XXII", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [55, 89, 115]}
    TR23 = {'title': "Trinity XXIII", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [52, 139, 163]}
    TR24 = {'title': "Trinity XXIV", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [26, 60]}
    TR25 = {'title': "Trinity XXV", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [90, 116]}
    TR26 = {'title': "Trinity XXVI", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [70]}
    TR27 = {'title': "Trinity XXVII", 'link': 'https://en.wikipedia.org/wiki/Trinity_Sunday', 'bwv': [140]}
    JOHN = {'title': "Nativity of Saint John the Baptist", 'link': 'https://en.wikipedia.org/wiki/Nativity_of_John_the_Baptist', 'bwv': [7, 30, 167]}
    MICH = {'title': "Michaelmas", 'link': 'https://en.wikipedia.org/wiki/Michaelmas', 'bwv': [19, 50, 130, 149]}
    VISI = {'title': "Visitation", 'link': 'https://en.wikipedia.org/wiki/Visitation_(Christianity)', 'bwv': [10, 147]}
    REFO = {'title': "Reformation Day", 'link': 'https://en.wikipedia.org/wiki/Reformation_Day', 'bwv': [79, 80]}


events = pd.DataFrame(columns=['Date', 'Event Type'])


def get_static_dates(year):
    events.loc[len(events)] = [f'{year}-12-25', EventType.CHR1.name]
    events.loc[len(events)] = [f'{year}-12-26', EventType.CHR2.name]
    events.loc[len(events)] = [f'{year}-12-27', EventType.CHR3.name]
    events.loc[len(events)] = [f'{year}-01-01', EventType.NYD1.name]
    events.loc[len(events)] = [f'{year}-01-02', EventType.NYD2.name]
    events.loc[len(events)] = [f'{year}-01-06', EventType.EPH0.name]
    events.loc[len(events)] = [f'{year}-02-02', EventType.PURI.name]
    events.loc[len(events)] = [f'{year}-06-24', EventType.JOHN.name]
    events.loc[len(events)] = [f'{year}-09-29', EventType.MICH.name]
    events.loc[len(events)] = [f'{year}-07-02', EventType.VISI.name]
    events.loc[len(events)] = [f'{year}-10-31', EventType.REFO.name]

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
    quas = eas1 + timedelta(weeks=1)
    mise = eas1 + timedelta(weeks=2)
    jubi = eas1 + timedelta(weeks=3)
    cant = eas1 + timedelta(weeks=4)
    roga = eas1 + timedelta(weeks=5)
    exau = eas1 + timedelta(weeks=6)
    asce = helpers.get_last_weekday(exau, 3)
    whi1 = exau + timedelta(weeks=1)
    whi2 = whi1 + timedelta(days=1)
    whi3 = whi1 + timedelta(days=2)

    # sunday after Christmas
    sunday_after_christmas = helpers.get_next_weekday(helpers.get_date_from_str(f'{year}-12-25'), 6)
    if sunday_after_christmas.year == year:
        events.loc[len(events)] = [sunday_after_christmas, EventType.CHR4.name]

    # Epiphany calculations
    eph1 = helpers.get_next_weekday(helpers.get_date_from_str(f'{year}-01-06'), 6)
    for index, key in enumerate([EventType.EPH1.name, EventType.EPH2.name, EventType.EPH3.name, EventType.EPH4.name]):
        date = eph1 + timedelta(weeks=index + 1)
        if date < sept:
            events.loc[len(events)] = [date, key]

    # Annunciation calculation - is condition right? - possibility of Annunciation on Saturday before Quasimodogeniti?
    annu = helpers.get_date_from_str(f'{year}-03-25')
    if annu >= palm:
        annu = quas + timedelta(days=1)

    # Trinity calculations
    event_types = [member.name for member in EventType]
    trinitatis = list(filter(lambda x: re.compile('TR').match(x), event_types))
    for index, key in enumerate(trinitatis):
        date = whi1 + timedelta(weeks=index + 1)
        if date < adv1:
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
    events.loc[len(events)] = [quas, EventType.QUAS.name]
    events.loc[len(events)] = [mise, EventType.MISE.name]
    events.loc[len(events)] = [jubi, EventType.JUBI.name]
    events.loc[len(events)] = [cant, EventType.CANT.name]
    events.loc[len(events)] = [roga, EventType.ROGA.name]
    events.loc[len(events)] = [exau, EventType.EXAU.name]
    events.loc[len(events)] = [asce, EventType.ASCE.name]
    events.loc[len(events)] = [annu, EventType.ANNU.name]
    events.loc[len(events)] = [whi1, EventType.WHI1.name]
    events.loc[len(events)] = [whi2, EventType.WHI2.name]
    events.loc[len(events)] = [whi3, EventType.WHI3.name]

    df = events.sort_values(by="Date")
    pprint(df)


if __name__ == '__main__':
    when = 2022
    get_static_dates(when)
    get_dynamic_dates(when)
