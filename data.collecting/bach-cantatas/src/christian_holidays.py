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


def calc_christmas(year):
    return date_from_str(f'{year}-12-25')


def int_to_roman(num):
    m = ["", "M", "MM", "MMM"]
    c = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
    x = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
    i = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]

    thousands = m[num // 1000]
    hundreds = c[(num % 1000) // 100]
    tens = x[(num % 100) // 10]
    ones = i[num % 10]

    return thousands + hundreds + tens + ones


class CalendarSeason:
    def __init__(self, title, url_link):
        self.title = title
        self.url_link = url_link


class ChristianHoliday:
    def __init__(self, title, url_link, labels=None, dates=None):
        if dates is None:
            dates = []
        if labels is None:
            labels = []
        self.title = title
        self.url_link = url_link
        self.labels = labels
        self.dates = dates

    def dates_for_holiday(self, holiday, years):
        for year in years:
            match holiday:
                case _ as holiday if 'ADVENT_' in holiday.name:
                    self.dates.append(self.__advents(year).get(holiday.name))
                case _ as holiday if 'CHRISTMAS_' in holiday.name:
                    self.dates.append(self.__christmas(year).get(holiday.name))
                case _ as holiday if 'EPIPHANY_' in holiday.name:
                    self.dates.append(self.__epiphany(year).get(holiday.name))
                case _ as holiday if LabelCalendarSeason.SHROVETIDE.value[0] in holiday.labels[0][0]:
                    self.dates.append(self.__shrovetide(year).get(holiday.name))
                case _ as holiday if LabelCalendarSeason.HOLY_WEEK.value[0] in holiday.labels[0][0]:
                    self.dates.append(self.__holy_week(year).get(holiday.name))
                case _ as holiday if LabelCalendarSeason.AFTER_EASTER.value[0] in holiday.labels[0][0]:
                    self.dates.append(self.__after_easter(year).get(holiday.name))
                case _ as holiday if 'WHIT_' in holiday.name:
                    self.dates.append(self.__whit(year).get(holiday.name))
                case _ as holiday if 'TRINITY_' in holiday.name:
                    trinity_data = self.__trinity(year).get(holiday.name)
                    if trinity_data is not None:
                        self.dates.append(trinity_data)
                case _:
                    pass

        return self

    @staticmethod
    def __advents(year):
        types = [church_year.name for church_year in ChurchYear]
        advents = list(filter(lambda x: re.compile('ADVENT').match(x), types))[:-1]

        ret_val = {}
        christmas = calc_christmas(year)
        advent_4 = last_weekday(christmas, 6)
        ret_val[ChurchYear.ADVENT_4.name] = advent_4

        for index, key in enumerate(advents):
            ret_val[key] = advent_4 - timedelta(weeks=len(advents) - index)

        return ret_val

    @staticmethod
    def __christmas(year):
        ret_val = {}
        christmas_1 = calc_christmas(year)
        ret_val[ChurchYear.CHRISTMAS_1.name] = christmas_1

        for index, key in enumerate([ChurchYear.CHRISTMAS_2.name, ChurchYear.CHRISTMAS_3.name]):
            ret_val[key] = christmas_1 + timedelta(days=index + 1)

        christmas_4 = next_weekday(christmas_1, 6)
        if christmas_4.year == year:
            ret_val[ChurchYear.CHRISTMAS_4.name] = christmas_4

        return ret_val

    # @staticmethod
    # def __new_year(year):
    #     return date_from_str(f'{year}-01-01')

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

    @staticmethod
    def __after_easter(year):
        ret_val = {}
        easter = calc_easter(year)
        sundays = [
            ChurchYear.QUASIMODOGENITI.name,
            ChurchYear.MISERICORDIAS_DOMINI.name,
            ChurchYear.JUBILATE.name,
            ChurchYear.CANTATE.name,
            ChurchYear.ROGATE.name,
            ChurchYear.EXAUDI.name
        ]

        for index, key in enumerate(sundays):
            ret_val[key] = easter + timedelta(weeks=index + 1)

        ret_val[ChurchYear.ASCENSION.name] = last_weekday(easter + timedelta(weeks=6), 3)

        return ret_val

    @staticmethod
    def __whit(year):
        easter = calc_easter(year)
        whit_1 = easter + timedelta(weeks=7)
        whit_2 = whit_1 + timedelta(days=1)
        whit_3 = whit_2 + timedelta(days=1)

        ret_val = {
            ChurchYear.WHIT_1.name: whit_1,
            ChurchYear.WHIT_2.name: whit_2,
            ChurchYear.WHIT_3.name: whit_3,
        }

        return ret_val

    @staticmethod
    def __trinity(year):
        christmas = calc_christmas(year)
        easter = calc_easter(year)
        advent_4 = last_weekday(christmas, 6)

        start_date = easter + timedelta(weeks=7)
        end_date = advent_4 - timedelta(weeks=3)

        types = [church_year.name for church_year in ChurchYear]
        trinitatis = list(filter(lambda x: re.compile('TRINITY_').match(x), types))
        ret_val = {}
        for index, key in enumerate(trinitatis):
            date = start_date + timedelta(weeks=index + 1)
            if date < end_date:
                ret_val[key] = start_date + timedelta(weeks=index + 1)

        return ret_val


class LabelCalendarSeason(CalendarSeason, Enum):
    ADVENT = 'Advent', 'https://en.wikipedia.org/wiki/Advent'
    CHRISTMAS = 'Christmas', 'https://en.wikipedia.org/wiki/Christmas'
    EPIPHANY = 'Epiphany', 'https://en.wikipedia.org/wiki/Epiphany_season'
    SHROVETIDE = 'Shrovetide', 'https://en.wikipedia.org/wiki/Shrovetide'
    HOLY_WEEK = 'Holy Week', 'https://en.wikipedia.org/wiki/Holy_Week'
    AFTER_EASTER = 'After Easter', ''
    WHIT = 'Whit', ''
    TRINITY = 'Trinity', ''


class LabelCalendarCycle(Enum):
    TEMPORAL = 'Temporal Cycle'
    SANCTORAL = 'Sanctoral Cycle'


def get_church_year_enum():
    # 'jak spocitat advent - objevuje se 30.11.'
    # 'nedele po Vanocich a po Novem roce?'
    ret_val = Enum(
        "ChurchYear",
        [
            ('ADVENT_1', ('Advent I', 'https://en.wikipedia.org/wiki/Advent', [LabelCalendarSeason.ADVENT.value, LabelCalendarCycle.TEMPORAL.value])),
            ('ADVENT_2', ('Advent II', 'https://en.wikipedia.org/wiki/Advent', [LabelCalendarSeason.ADVENT.value, LabelCalendarCycle.TEMPORAL.value])),
            ('ADVENT_3', ('Advent III', 'https://en.wikipedia.org/wiki/Advent', [LabelCalendarSeason.ADVENT.value, LabelCalendarCycle.TEMPORAL.value])),
            ('ADVENT_4', ('Advent IV', 'https://en.wikipedia.org/wiki/Advent', [LabelCalendarSeason.ADVENT.value, LabelCalendarCycle.TEMPORAL.value])),
            ('CHRISTMAS_1', ('Christmas Day', 'https://en.wikipedia.org/wiki/Christmas', [LabelCalendarSeason.CHRISTMAS.value, LabelCalendarCycle.TEMPORAL.value])),
            ('CHRISTMAS_2', ("Saint Stephen's Day", 'https://en.wikipedia.org/wiki/Saint_Stephen%27s_Day', [LabelCalendarSeason.CHRISTMAS.value, LabelCalendarCycle.TEMPORAL.value])),
            ('CHRISTMAS_3', ('Third day of Christmas', 'https://en.wikipedia.org/wiki/Christmas', [LabelCalendarSeason.CHRISTMAS.value, LabelCalendarCycle.TEMPORAL.value])),
            ('CHRISTMAS_4', ('Sunday after Christmas', 'https://en.wikipedia.org/wiki/Christmas_Sunday', [LabelCalendarSeason.CHRISTMAS.value, LabelCalendarCycle.TEMPORAL.value])),]
        + generate_data_for_church_year_enum(
            7,
            'Epiphany',
            'https://en.wikipedia.org/wiki/Epiphany_(holiday)',
            [LabelCalendarSeason.EPIPHANY, LabelCalendarCycle.TEMPORAL]
        ) +
        [
            ('SEPTUAGESIMA', ('Septuagesima', 'https://en.wikipedia.org/wiki/Septuagesima', [LabelCalendarSeason.SHROVETIDE.value, LabelCalendarCycle.TEMPORAL.value])),
            ('SEXAGESIMA', ('Sexagesima', 'https://en.wikipedia.org/wiki/Sexagesima', [LabelCalendarSeason.SHROVETIDE.value, LabelCalendarCycle.TEMPORAL.value])),
            ('QUINQUAGESIMA', ('Quinquagesima', 'https://en.wikipedia.org/wiki/Quinquagesima', [LabelCalendarSeason.SHROVETIDE.value, LabelCalendarCycle.TEMPORAL.value])),
            ('PALM_SUNDAY', ('Palm Sunday', 'https://en.wikipedia.org/wiki/Palm_Sunday', [LabelCalendarSeason.HOLY_WEEK.value, LabelCalendarCycle.TEMPORAL.value])),
            ('GOOD_FRIDAY', ('Good Friday', 'https://en.wikipedia.org/wiki/Good_Friday', [LabelCalendarSeason.HOLY_WEEK.value, LabelCalendarCycle.TEMPORAL.value])),
            ('HOLY_SATURDAY', ('Holy Saturday', 'https://en.wikipedia.org/wiki/Holy_Saturday', [LabelCalendarSeason.HOLY_WEEK.value, LabelCalendarCycle.TEMPORAL.value])),
            ('EASTER', ('Easter', 'https://en.wikipedia.org/wiki/Easter', [LabelCalendarSeason.HOLY_WEEK.value, LabelCalendarCycle.TEMPORAL.value])),
            ('QUASIMODOGENITI', ('Second Sunday of Easter (Quasimodogeniti)', 'https://en.wikipedia.org/wiki/Second_Sunday_of_Easter', [LabelCalendarSeason.AFTER_EASTER.value, LabelCalendarCycle.TEMPORAL.value])),
            ('MISERICORDIAS_DOMINI', ('Third Sunday of Easter (Misericordias Domini)', 'https://en.wikipedia.org/wiki/Third_Sunday_of_Easter', [LabelCalendarSeason.AFTER_EASTER.value, LabelCalendarCycle.TEMPORAL.value])),
            ('JUBILATE', ('Fourth Sunday of Easter (Jubilate)', 'https://en.wikipedia.org/wiki/Fourth_Sunday_of_Easter', [LabelCalendarSeason.AFTER_EASTER.value, LabelCalendarCycle.TEMPORAL.value])),
            ('CANTATE', ('Fifth Sunday of Easter (Cantate)', 'https://en.wikipedia.org/wiki/Fifth_Sunday_of_Easter', [LabelCalendarSeason.AFTER_EASTER.value, LabelCalendarCycle.TEMPORAL.value])),
            ('ROGATE', ('Sixth Sunday of Easter (Rogate)', 'https://en.wikipedia.org/wiki/Rogation_days', [LabelCalendarSeason.AFTER_EASTER.value, LabelCalendarCycle.TEMPORAL.value])),
            ('ASCENSION', ('Holy Thursday (Ascension)', 'https://en.wikipedia.org/wiki/Feast_of_the_Ascension', [LabelCalendarSeason.AFTER_EASTER.value, LabelCalendarCycle.TEMPORAL.value])),
            ('EXAUDI', ('Sunday after the Ascension (Exaudi)', 'https://www.csmedia1.com/ziondetroit.org/exaudi.pdf', [LabelCalendarSeason.AFTER_EASTER.value, LabelCalendarCycle.TEMPORAL.value])),
            ('WHIT_1', ('Whit Sunday (Pentecost)', 'https://en.wikipedia.org/wiki/Pentecost', [LabelCalendarSeason.WHIT.value, LabelCalendarCycle.TEMPORAL.value])),
            ('WHIT_2', ('Whit Monday', 'https://en.wikipedia.org/wiki/Whit_Monday', [LabelCalendarSeason.WHIT.value, LabelCalendarCycle.TEMPORAL.value])),
            ('WHIT_3', ('Whit Tuesday', 'https://en.wikipedia.org/wiki/Whit_Tuesday', [LabelCalendarSeason.WHIT.value, LabelCalendarCycle.TEMPORAL.value])),
        ]
        + generate_data_for_church_year_enum(
            28,
            'trinity',
            'https://en.wikipedia.org/wiki/Trinity_Sunday',
            [LabelCalendarSeason.TRINITY, LabelCalendarCycle.TEMPORAL]
        ),
        type=ChristianHoliday)

    return ret_val


# class ChurchYear(ChristianHoliday, Enum):
#     ADVENT_1 = 'Advent I', 'https://en.wikipedia.org/wiki/Advent', [LabelCalendarSeason.ADVENT.value, LabelCalendarCycle.TEMPORAL.value]
#     ADVENT_2 = 'Advent II', 'https://en.wikipedia.org/wiki/Advent', [LabelCalendarSeason.ADVENT.value,
#                                                                      LabelCalendarCycle.TEMPORAL.value]
#     ADVENT_3 = 'Advent III', 'https://en.wikipedia.org/wiki/Advent', [LabelCalendarSeason.ADVENT.value,
#                                                                       LabelCalendarCycle.TEMPORAL.value]
#     ADVENT_4 = 'Advent IV', 'https://en.wikipedia.org/wiki/Advent', [LabelCalendarSeason.ADVENT.value,
#                                                                      LabelCalendarCycle.TEMPORAL.value]
#     CHRISTMAS_1 = 'Christmas Day', 'https://en.wikipedia.org/wiki/Christmas', [LabelCalendarSeason.CHRISTMAS.value,
#                                                                                LabelCalendarCycle.TEMPORAL.value]
#     CHRISTMAS_2 = "Saint Stephen's Day", 'https://en.wikipedia.org/wiki/Saint_Stephen%27s_Day', [
#         LabelCalendarSeason.CHRISTMAS.value, LabelCalendarCycle.TEMPORAL.value]
#     CHRISTMAS_3 = 'Third day of Christmas', 'https://en.wikipedia.org/wiki/Christmas', [
#         LabelCalendarSeason.CHRISTMAS.value, LabelCalendarCycle.TEMPORAL.value]
#     CHRISTMAS_4 = 'Sunday after Christmas', 'https://en.wikipedia.org/wiki/Christmas_Sunday', [
#         LabelCalendarSeason.CHRISTMAS.value, LabelCalendarCycle.TEMPORAL.value]
#     # nebo nazev po Novem roce
#     EPIPHANY_1 = 'Epiphany', 'https://en.wikipedia.org/wiki/Epiphany_(holiday)', [LabelCalendarSeason.EPIPHANY.value,
#                                                                                   LabelCalendarCycle.TEMPORAL.value]
#     EPIPHANY_2 = 'Epiphany I', 'https://en.wikipedia.org/wiki/Epiphany_(holiday)', [LabelCalendarSeason.EPIPHANY.value,
#                                                                                     LabelCalendarCycle.TEMPORAL.value]
#     EPIPHANY_3 = 'Epiphany II', 'https://en.wikipedia.org/wiki/Epiphany_(holiday)', [LabelCalendarSeason.EPIPHANY.value,
#                                                                                      LabelCalendarCycle.TEMPORAL.value]
#     EPIPHANY_4 = 'Epiphany III', 'https://en.wikipedia.org/wiki/Epiphany_(holiday)', [
#         LabelCalendarSeason.EPIPHANY.value, LabelCalendarCycle.TEMPORAL.value]
#     EPIPHANY_5 = 'Epiphany IV', 'https://en.wikipedia.org/wiki/Epiphany_(holiday)', [LabelCalendarSeason.EPIPHANY.value,
#                                                                                      LabelCalendarCycle.TEMPORAL.value]
#     EPIPHANY_6 = 'Epiphany V', 'https://en.wikipedia.org/wiki/Epiphany_(holiday)', [LabelCalendarSeason.EPIPHANY.value,
#                                                                                     LabelCalendarCycle.TEMPORAL.value]
#     # CANDLEMAS = 'Candlemas', 'https://en.wikipedia.org/wiki/Candlemas'
#     # 'https://en.wikipedia.org/wiki/Presentation_of_Jesus_at_the_Temple'
#     SEPTUAGESIMA = 'Septuagesima', 'https://en.wikipedia.org/wiki/Septuagesima', [LabelCalendarSeason.SHROVETIDE.value,
#                                                                                   LabelCalendarCycle.TEMPORAL.value]
#     SEXAGESIMA = 'Sexagesima', 'https://en.wikipedia.org/wiki/Sexagesima', [LabelCalendarSeason.SHROVETIDE.value,
#                                                                             LabelCalendarCycle.TEMPORAL.value]
#     QUINQUAGESIMA = 'Quinquagesima', 'https://en.wikipedia.org/wiki/Quinquagesima', [
#         LabelCalendarSeason.SHROVETIDE.value, LabelCalendarCycle.TEMPORAL.value]
#     PALM_SUNDAY = 'Palm Sunday', 'https://en.wikipedia.org/wiki/Palm_Sunday', [LabelCalendarSeason.HOLY_WEEK.value,
#                                                                                LabelCalendarCycle.TEMPORAL.value]
#     GOOD_FRIDAY = 'Good Friday', 'https://en.wikipedia.org/wiki/Good_Friday', [LabelCalendarSeason.HOLY_WEEK.value,
#                                                                                LabelCalendarCycle.TEMPORAL.value]
#     HOLY_SATURDAY = 'Holy Saturday', 'https://en.wikipedia.org/wiki/Holy_Saturday', [
#         LabelCalendarSeason.HOLY_WEEK.value, LabelCalendarCycle.TEMPORAL.value]
#     EASTER = 'Easter', 'https://en.wikipedia.org/wiki/Easter', [LabelCalendarSeason.HOLY_WEEK.value,
#                                                                 LabelCalendarCycle.TEMPORAL.value]
#
#     QUASIMODOGENITI = 'Second Sunday of Easter (Quasimodogeniti)', 'https://en.wikipedia.org/wiki/Second_Sunday_of_Easter', [
#         LabelCalendarSeason.AFTER_EASTER.value, LabelCalendarCycle.TEMPORAL.value]
#     MISERICORDIAS_DOMINI = 'Third Sunday of Easter (Misericordias Domini)', 'https://en.wikipedia.org/wiki/Third_Sunday_of_Easter', [
#         LabelCalendarSeason.AFTER_EASTER.value, LabelCalendarCycle.TEMPORAL.value]
#     JUBILATE = 'Fourth Sunday of Easter (Jubilate)', 'https://en.wikipedia.org/wiki/Fourth_Sunday_of_Easter', [
#         LabelCalendarSeason.AFTER_EASTER.value, LabelCalendarCycle.TEMPORAL.value]
#     CANTATE = 'Fifth Sunday of Easter (Cantate)', 'https://en.wikipedia.org/wiki/Fifth_Sunday_of_Easter', [
#         LabelCalendarSeason.AFTER_EASTER.value, LabelCalendarCycle.TEMPORAL.value]
#     ROGATE = 'Sixth Sunday of Easter (Rogate)', 'https://en.wikipedia.org/wiki/Rogation_days', [
#         LabelCalendarSeason.AFTER_EASTER.value, LabelCalendarCycle.TEMPORAL.value]
#     ASCENSION = 'Holy Thursday (Ascension)', 'https://en.wikipedia.org/wiki/Feast_of_the_Ascension', [
#         LabelCalendarSeason.AFTER_EASTER.value, LabelCalendarCycle.TEMPORAL.value]
#     EXAUDI = 'Sunday after the Ascension (Exaudi)', 'https://www.csmedia1.com/ziondetroit.org/exaudi.pdf', [
#         LabelCalendarSeason.AFTER_EASTER.value, LabelCalendarCycle.TEMPORAL.value]
#     WHIT_1 = 'Whit Sunday (Pentecost)', 'https://en.wikipedia.org/wiki/Pentecost', [LabelCalendarSeason.WHIT.value,
#                                                                                     LabelCalendarCycle.TEMPORAL.value]
#     WHIT_2 = 'Whit Monday', 'https://en.wikipedia.org/wiki/Whit_Monday', [LabelCalendarSeason.WHIT.value,
#                                                                           LabelCalendarCycle.TEMPORAL.value]
#     WHIT_3 = 'Whit Tuesday', 'https://en.wikipedia.org/wiki/Whit_Tuesday', [LabelCalendarSeason.WHIT.value,
#                                                                             LabelCalendarCycle.TEMPORAL.value]
#
#
def generate_data_for_church_year_enum(count, name, link, labels):
    index = 0
    ret_val = []
    while index < count:
        obj = name.upper() + '_' + str(index + 1), (
            (name.capitalize() + ' ' + int_to_roman(index)).rstrip(),
            link,
            list(map(lambda label: label.value, labels)))
        ret_val.append(obj)
        index += 1

    return ret_val


ChurchYear = get_church_year_enum()


def christian_holidays():
    holidays = []
    for member in ChurchYear:
        holidays.append(member.dates_for_holiday(member, range(2022, 2023)))

    df = pd.DataFrame([vars(t) for t in holidays]).loc[:, ['title', 'url_link', 'labels', 'dates']]
    df.to_csv("test.csv", index=False)
