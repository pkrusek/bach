from enum import Enum
import re
from datetime import datetime, timedelta
import pandas as pd


def date_from_str(date_str):
    """
    Converts given date string in format 'YYYY.MM.DD' to date object.

    :param: date_str: str
    :return: date
    """
    return datetime.strptime(date_str, '%Y-%m-%d')


def last_weekday(in_date, weekday):
    """
    Returns previous day by week index.

    :param: in_date: date
        Given date.
    :param: weekday: int
        Given number with weekday index (0 = Monday).

    :return: Date
        A date object with desired date.
    """
    closest = in_date + timedelta(days=(weekday - in_date.weekday()))

    return closest if closest < in_date \
        else closest - timedelta(days=7)


def next_weekday(in_date, weekday):
    """
    Returns next day by week index.

    :param: in_date: date
        Given date.
    :param: weekday: int
        Given number with weekday index (0 = Monday).

    :return: Date
        A date object with desired date.
    """
    closest = in_date - timedelta(days=(in_date.weekday() - weekday))

    return closest if closest > in_date \
        else closest + timedelta(days=7)


def calc_easter(year):
    """
    Returns Easter as a date object by using Butcher's algorithm

    :param: year: int
        Given year.
    :return:
        Date object with Easter sunday.
    """
    a = year % 19
    b = year // 100
    c = year % 100
    d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
    e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
    f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
    month = f // 31
    day = f % 31 + 1

    return datetime(year, month, day)


class ChristianGroup:
    def __init__(self, title, url_link):
        self.title = title
        self.url_link = url_link


class ChristianHoliday:
    def __init__(self, title, url_link, group='', dates=None):
        if dates is None:
            dates = []
        self.title = title
        self.url_link = url_link
        self.group = group
        self.dates = dates

    def dates_for_holiday(self, holiday):
        for year in range(2022, 2023):
            match holiday:
                case ChurchYear.ADVENT_1 | ChurchYear.ADVENT_2 | ChurchYear.ADVENT_3 | ChurchYear.ADVENT_4:
                    self.dates.append(self.__advents(year).get(holiday.name))
                case ChurchYear.CHRISTMAS_1 | ChurchYear.CHRISTMAS_2 | ChurchYear.CHRISTMAS_3 | ChurchYear.CHRISTMAS_4:
                    self.dates.append(self.__christmas(year).get(holiday.name))
                case ChurchYear.PALM_SUNDAY | ChurchYear.GOOD_FRIDAY | ChurchYear.HOLY_SATURDAY | ChurchYear.EASTER:
                    self.dates.append(self.__holy_week(year).get(holiday.name))
                case ChurchYear.SEXAGESIMA | ChurchYear.SEPTUAGESIMA | ChurchYear.QUINQUAGESIMA:
                    self.dates.append(self.__shrovetide(year).get(holiday.name))
                case ChurchYear.EPIPHANY_1:
                    self.__epiphany(year)
                case _:
                    pass

        return self

    def __advents(self, year):
        types = [church_year.name for church_year in ChurchYear]
        advents = list(filter(lambda x: re.compile('ADVENT').match(x), types))[: -1]

        ret_val = {}
        advent_4 = last_weekday(self.__christmas(year)[ChurchYear.CHRISTMAS_1.name], 6)
        ret_val[ChurchYear.ADVENT_4.name] = advent_4

        for index, key in enumerate(advents):
            ret_val[key] = advent_4 - timedelta(weeks=len(advents) - index)

        return ret_val

    @staticmethod
    def __christmas(year):
        ret_val = {}
        christmas_1 = date_from_str(f'{year}-12-25')
        ret_val[ChurchYear.CHRISTMAS_1.name] = christmas_1

        for index, key in enumerate([ChurchYear.CHRISTMAS_2.name, ChurchYear.CHRISTMAS_3.name]):
            ret_val[key] = christmas_1 + timedelta(days=index + 1)

        christmas_4 = next_weekday(christmas_1, 6)
        if christmas_4.year == year:
            ret_val[ChurchYear.CHRISTMAS_4.name] = christmas_4

        return ret_val

    @staticmethod
    def __new_year(year):
        return date_from_str(f'{year}-01-01')

    @staticmethod
    def __epiphany(year):
        ret_val = {}
        epiphany_1 = date_from_str(f'{year}-01-06')
        ret_val[ChurchYear.EPIPHANY_1.name] = epiphany_1

        types = [church_year.name for church_year in ChurchYear]
        epiphany = list(filter(lambda x: re.compile('EPIPHANY').match(x), types))
        epiphany.pop(0)

        easter = calc_easter(year)
        quinquagesima = easter - timedelta(weeks=7)
        for index, key in enumerate(epiphany):
            date = epiphany_1 + timedelta(weeks=index + 1)
            if date < quinquagesima:
                ret_val[key] = date

        return ret_val

    @staticmethod
    def __shrovetide(year):
        easter = calc_easter(year)
        quinquagesima = easter - timedelta(weeks=7)
        sexagesima = quinquagesima - timedelta(weeks=1)
        septuagesima = sexagesima - timedelta(weeks=1)

        ret_val = {
            ChurchYear.SEXAGESIMA.name: sexagesima,
            ChurchYear.SEPTUAGESIMA.name: septuagesima,
            ChurchYear.QUINQUAGESIMA.name: quinquagesima
        }

        return ret_val

    @staticmethod
    def __holy_week(year):
        easter = calc_easter(year)
        palm_sunday = easter - timedelta(weeks=1)
        good_friday = last_weekday(easter, 4)
        good_saturday = last_weekday(easter, 5)

        ret_val = {
            ChurchYear.PALM_SUNDAY.name: palm_sunday,
            ChurchYear.GOOD_FRIDAY.name: good_friday,
            ChurchYear.HOLY_SATURDAY.name: good_saturday,
            ChurchYear.EASTER.name: easter
        }

        return ret_val


class ChurchGroup(ChristianGroup, Enum):
    ADVENT = 'Advent', 'https://en.wikipedia.org/wiki/Advent'
    CHRISTMAS = 'Christmas', 'https://en.wikipedia.org/wiki/Christmas'
    EPIPHANY = 'Epiphany', 'https://en.wikipedia.org/wiki/Epiphany_season'
    SHROVETIDE = 'Shrovetide', 'https://en.wikipedia.org/wiki/Shrovetide'
    HOLY_WEEK = 'Holy Week', 'https://en.wikipedia.org/wiki/Holy_Week'


class ChurchYear(ChristianHoliday, Enum):
    ADVENT_1 = 'Advent I', 'https://en.wikipedia.org/wiki/Advent', ChurchGroup.ADVENT.value
    ADVENT_2 = 'Advent II', 'https://en.wikipedia.org/wiki/Advent', ChurchGroup.ADVENT.value
    ADVENT_3 = 'Advent III', 'https://en.wikipedia.org/wiki/Advent', ChurchGroup.ADVENT.value
    ADVENT_4 = 'Advent IV', 'https://en.wikipedia.org/wiki/Advent', ChurchGroup.ADVENT.value
    CHRISTMAS_1 = 'Christmas Day', 'https://en.wikipedia.org/wiki/Christmas', ChurchGroup.CHRISTMAS.value
    CHRISTMAS_2 = "Saint Stephen's Day", 'https://en.wikipedia.org/wiki/Saint_Stephen%27s_Day', ChurchGroup.CHRISTMAS.value
    CHRISTMAS_3 = 'Third day of Christmas', 'https://en.wikipedia.org/wiki/Christmas', ChurchGroup.CHRISTMAS.value
    CHRISTMAS_4 = 'Sunday after Christmas', 'https://en.wikipedia.org/wiki/Christmas_Sunday', ChurchGroup.CHRISTMAS.value
    # nebo nazev po Novem roce
    EPIPHANY_1 = 'Epiphany', 'https://en.wikipedia.org/wiki/Epiphany_(holiday)', ChurchGroup.EPIPHANY.value
    EPIPHANY_2 = 'Epiphany I', 'https://en.wikipedia.org/wiki/Epiphany_(holiday)', ChurchGroup.EPIPHANY.value
    EPIPHANY_3 = 'Epiphany II', 'https://en.wikipedia.org/wiki/Epiphany_(holiday)', ChurchGroup.EPIPHANY.value
    EPIPHANY_4 = 'Epiphany III', 'https://en.wikipedia.org/wiki/Epiphany_(holiday)', ChurchGroup.EPIPHANY.value
    EPIPHANY_5 = 'Epiphany IV', 'https://en.wikipedia.org/wiki/Epiphany_(holiday)', ChurchGroup.EPIPHANY.value
    EPIPHANY_6 = 'Epiphany V', 'https://en.wikipedia.org/wiki/Epiphany_(holiday)', ChurchGroup.EPIPHANY.value
    # how many epiphany?
    SEPTUAGESIMA = 'Septuagesima', 'https://en.wikipedia.org/wiki/Septuagesima', ChurchGroup.SHROVETIDE.value
    SEXAGESIMA = 'Sexagesima', 'https://en.wikipedia.org/wiki/Sexagesima', ChurchGroup.SHROVETIDE.value
    QUINQUAGESIMA = 'Quinquagesima', 'https://en.wikipedia.org/wiki/Quinquagesima', ChurchGroup.SHROVETIDE.value
    PALM_SUNDAY = 'Palm Sunday', 'https://en.wikipedia.org/wiki/Palm_Sunday', ChurchGroup.HOLY_WEEK.value
    GOOD_FRIDAY = 'Good Friday', 'https://en.wikipedia.org/wiki/Good_Friday', ChurchGroup.HOLY_WEEK.value
    HOLY_SATURDAY = 'Holy Saturday', 'https://en.wikipedia.org/wiki/Holy_Saturday', ChurchGroup.HOLY_WEEK.value
    EASTER = 'Easter', 'https://en.wikipedia.org/wiki/Easter', ChurchGroup.HOLY_WEEK.value


if __name__ == '__main__':
    holidays = []

    print("Sexagesima".upper())
    for member in ChurchYear:
        # print(member)
        holidays.append(member.dates_for_holiday(member))

    # print(holidays)
    df = pd.DataFrame([vars(t) for t in holidays]).loc[:, ['title', 'url_link', 'group', 'dates']]
    # df['group'].str.split(' ', expand=True).set_axis(['Number', 'Letter'], axis='group')
    df.to_csv("test.csv", index=False)
