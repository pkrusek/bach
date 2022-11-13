"""
This module generates the Lutheran Church Year. 
"""
# pylint: disable=no-member
from __future__ import annotations

from datetime import datetime, timedelta
import re
from enum import Enum
import pandas as pd


def date_from_str(date_str: str) -> datetime:
    """
    Converts given date string in format 'YYYY-MM-DD' to datetime object.

    :param: date_str
    :return: string converted to date
    """
    return datetime.strptime(date_str, '%Y-%m-%d')


def last_weekday(in_date: datetime, weekday: int) -> datetime:
    """
    Returns previous day by week index.

    :param: in_date: Given date.
    :param: weekday: Given number with weekday index (0 = Monday).

    :return: A datetime object with desired date.
    """
    closest = in_date + timedelta(days=(weekday - in_date.weekday()))

    return closest if closest < in_date \
        else closest - timedelta(days=7)


def next_weekday(in_date: datetime, weekday: int) -> datetime:
    """
    Returns next day by week index.

    :param: in_date: Given date.
    :param: weekday: Given number with weekday index (0 = Monday).

    :return: A datetime object with desired date.
    """
    closest = in_date - timedelta(days=(in_date.weekday() - weekday))

    return closest if closest > in_date \
        else closest + timedelta(days=7)


def calc_easter(year: int) -> datetime:
    """
    Returns Easter as a datetime object by using Butcher's algorithm.
    Easter (the Resurrection of Christ) is related to the full moon,
    as it is Easter the first Sunday after full moon after vernal equinox.

    :param: year: Given year.
    :return: Datetime object with Easter sunday.
    """
    # pylint: disable=invalid-name
    a = year % 19
    b = year // 100
    c = year % 100
    d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
    e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
    f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
    month = f // 31
    day = f % 31 + 1

    return datetime(year, month, day)


def calc_christmas(year: int) -> datetime:
    """
    Returns a datetime object with Christmas day for given year.
    Christmas, the birth of Christ is always the 25th of December.

    :param year: Given year.
    :type year: int
    :return: Datetime object - Christmas date.
    :rtype: datetime
    """
    return date_from_str(f'{year}-12-25')


def int_to_roman(num: int) -> str:
    """
    Converts given integer to roman numeral.

    :param num: Given integer.
    :type num: int
    :return: String with roman numeral. 
    :rtype: str
    """
    # pylint: disable=invalid-name
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
    def __init__(  # pylint: disable=too-many-arguments
            self, title, url_link, labels=None, dates=None, ident=''
    ):
        if dates is None:
            dates = []
        if labels is None:
            labels = []
        self.title = title
        self.url_link = url_link
        self.labels = labels
        self.dates = dates
        self.ident = ident

    def dates_for_holiday(self, holiday: ChurchYear, years: range) -> ChristianHoliday:
        """
        Returns itself with generated dates in given year's range.

        :param holiday: given enum value with certain holiday.
        :type holiday: ChurchYear
        :param years: given year's range.
        :type years: range
        :return: self.
        :rtype: ChristianHoliday
        """
        for year in years:
            match holiday:
                case _ as holiday if 'ADVENT_' in holiday.name:
                    self.calc_dates_for(self.__advents, holiday, year)
                case _ as holiday if 'CHRISTMAS_' in holiday.name:
                    self.calc_dates_for(self.__christmas, holiday, year)
                case _ as holiday if 'NEW_YEAR_' in holiday.name:
                    self.calc_dates_for(self.__new_year, holiday, year)
                case _ as holiday if 'EPIPHANY_' in holiday.name:
                    self.calc_dates_for(self.__epiphany, holiday, year)
                case _ as holiday if LabelCalendarSeason.SHROVETIDE.value[0] in holiday.labels[0][0]:
                    self.calc_dates_for(self.__shrovetide, holiday, year)
                case _ as holiday if LabelCalendarSeason.HOLY_WEEK.value[0] in holiday.labels[0][0]:
                    self.calc_dates_for(self.__holy_week, holiday, year)
                case _ as holiday if LabelCalendarSeason.AFTER_EASTER.value[0] in holiday.labels[0][0]:
                    self.calc_dates_for(self.__after_easter, holiday, year)
                case _ as holiday if 'WHIT_' in holiday.name:
                    self.calc_dates_for(self.__whit, holiday, year)
                case _ as holiday if 'TRINITY_' in holiday.name:
                    self.calc_dates_for(self.__trinity, holiday, year)
                    # trinity_data = self.calc_dates_for(self.__trinity, holiday, year)
                    # if trinity_data is not None: #poresit v Pandas
                    #     self.dates.append(trinity_data)
                case _ as holiday if LabelCalendarSeason.STATIC.value[0] in holiday.labels[0][0]:
                    self.calc_dates_for(self.__static_dates, holiday, year)
                case _:
                    pass

        return self

    def calc_dates_for(self, method_to_run: any, holiday: ChristianHoliday, year: int) -> None:
        """
        Helper method for certain holiday dates calculation.

        :param method_to_run: method to run.
        :type method_to_run: any
        :param holiday: target holiday.
        :type holiday: ChristianHoliday
        :param year: given year.
        :type year: int
        """
        self.dates.append(method_to_run(year).get(holiday.name))

    @staticmethod
    def __advents(year: int) -> dict:
        """
        Calculates all advent dates for a given year.
        Four Sundays before Chrismas the new Church Year begins - 1st, 2nd, 3rd and 4th Sunday in Advent.

        :param year: given year.
        :type year: int
        :return: dictionary with ChurchYear enum's name as key and date as value.
        :rtype: dict
        """
        types = [church_year.name for church_year in ChurchYear]
        advents = list(filter(lambda x: re.compile('ADVENT').match(x), types))[:-1]

        ret_val = {}
        christmas = calc_christmas(year)
        advent_4 = last_weekday(christmas, 6)

        for index, key in enumerate(advents):
            ret_val[key] = advent_4 - timedelta(weeks=len(advents) - index)

        ret_val[ChurchYear.ADVENT_4.name] = advent_4

        return ret_val

    @staticmethod
    def __christmas(year: int) -> dict:
        """
        Calculates all dates related to Christmas for a given year.
        1. Christmas itself.
        2. Next day after Christmas (26th of December) - St. Stefanus Day (in remembrance of the first Christian martyr: Stefanus) or 2nd Day of Christmas.
        3. 3rd Day of Christmas.

        :param year: given year.
        :type year: int
        :return: dictionary with ChurchYear enum's name as key and date as value.
        :rtype: dict
        """
        ret_val = {}
        christmas_1 = calc_christmas(year)
        ret_val[ChurchYear.CHRISTMAS_1.name] = christmas_1

        for index, key in enumerate([ChurchYear.CHRISTMAS_2.name, ChurchYear.CHRISTMAS_3.name]):
            ret_val[key] = christmas_1 + timedelta(days=index + 1)

        christmas_4 = next_weekday(christmas_1, 6)
        if christmas_4.year == year:
            ret_val[ChurchYear.CHRISTMAS_4.name] = christmas_4

        return ret_val

    @staticmethod
    def __new_year(year: int) -> dict:
        """
        Calculates all dates related to New Year for a given year.
        1. New Year.
        2. Day after New Year.

        :param year: given year.
        :type year: int
        :return: dictionary with ChurchYear enum's name as key and date as value.
        :rtype: dict
        """
        ny_1 = date_from_str(f'{year}-01-01')
        ny_2 = date_from_str(f'{year}-01-02')

        return {
            ChurchYear.NEW_YEAR_1.name: ny_1,
            ChurchYear.NEW_YEAR_2.name: ny_2,
        }

    @staticmethod
    def __epiphany(year: int) -> dict:
        """
        Calculates all dates related to Epiphany for a given year.
        1. Epiphany - the 6th of January (where the 3 Holy Kings visited Jesus).
        2. Further Epiphany - counting the remaining Sundays (there are maximum of 6), until reach Septuagesima.

        :param year: given year.
        :type year: int
        :return: dictionary with ChurchYear enum's name as key and date as value.
        :rtype: dict
        """
        ret_val = {}
        epiphany_1 = date_from_str(f'{year}-01-06')
        ret_val[ChurchYear.EPIPHANY_1.name] = epiphany_1

        types = [church_year.name for church_year in ChurchYear]
        epiphany = list(filter(lambda x: re.compile('EPIPHANY').match(x), types))
        epiphany.pop(0)

        easter = calc_easter(year)
        # quinquagesima = easter - timedelta(weeks=7)
        septuagesima = easter - timedelta(weeks=9)

        for index, key in enumerate(epiphany):
            date = epiphany_1 + timedelta(weeks=index + 1)
            if date < septuagesima:
                ret_val[key] = date

        return ret_val

    @staticmethod
    def __shrovetide(year: int) -> dict:
        """
        Calculates all dates related to Pre-Lenten Season.
        1. Sexagesima - Two Sundays before Estomihi.
        2. Septuagesima - Sunday before Estomihi.
        3. Quinquagesima (Estomihi) - last Sunday nefore Lent begins.

        :param year: given year.
        :type year: int
        :return: dictionary with ChurchYear enum's name as key and date as value.
        :rtype: dict
        """
        easter = calc_easter(year)
        quinquagesima = easter - timedelta(weeks=7)
        sexagesima = quinquagesima - timedelta(weeks=1)
        septuagesima = quinquagesima - timedelta(weeks=2)

        ret_val = {
            ChurchYear.SEXAGESIMA.name: sexagesima,
            ChurchYear.SEPTUAGESIMA.name: septuagesima,
            ChurchYear.QUINQUAGESIMA.name: quinquagesima
        }

        return ret_val

    @staticmethod
    def __holy_week(year: int) -> dict:
        """
        Calculates all dates related to Easter.
        1. Palm Sunday - one week before Easter.
        2. Good Friday (where Jesus was crucified) is the last Friday before Easter Sunday.
        3. Holy Saturday - Saturday between Good Friday and Easter.
        4. Easter Sunday.
        5. Easter Monday.
        6. Easter Tuesday.

        :param year: given year.
        :type year: int
        :return: dictionary with ChurchYear enum's name as key and date as value.
        :rtype: dict
        """
        easter = calc_easter(year)
        palm_sunday = easter - timedelta(weeks=1)
        good_friday = last_weekday(easter, 4)
        holy_saturday = last_weekday(easter, 5)
        easter_monday = easter + timedelta(days=1)
        easter_tuesday = easter + timedelta(days=2)

        ret_val = {
            ChurchYear.PALM_SUNDAY.name: palm_sunday,
            ChurchYear.GOOD_FRIDAY.name: good_friday,
            ChurchYear.HOLY_SATURDAY.name: holy_saturday,
            ChurchYear.EASTER_1.name: easter,
            ChurchYear.EASTER_2.name: easter_monday,
            ChurchYear.EASTER_3.name: easter_tuesday,
        }

        return ret_val

    @staticmethod
    def __after_easter(year: int) -> dict:
        """
        Calculates all dates after Easter and before Whit.
        1. Quasimodogeniti - 1st Sunday after Easter.
        2. Misericordias Domini - 2nd Sunday after Easter.
        3. Jubilate - 3rd Sunday after Easter.
        4. Cantate - 4th Sunday after Easter.
        5. Rogate - 5th Sunday after Easter.
        6. Ascension - Thursday between Rogate and Exaudi (40 days after Easter where Jesus ascended to Heaven).
        7. Exaudi - 6th Sunday after Easter.

        :param year: given year.
        :type year: int
        :return: dictionary with ChurchYear enum's name as key and date as value.
        :rtype: dict
        """
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
    def __whit(year: int) -> dict:
        """
        Calculates all dates related to Whit.

        :param year: given year.
        :type year: int
        :return: dictionary with ChurchYear enum's name as key and date as value.
        :rtype: dict
        """
        easter = calc_easter(year)
        whit_1 = easter + timedelta(weeks=7)
        whit_2 = whit_1 + timedelta(days=1)
        whit_3 = whit_1 + timedelta(days=2)

        ret_val = {
            ChurchYear.WHIT_1.name: whit_1,
            ChurchYear.WHIT_2.name: whit_2,
            ChurchYear.WHIT_3.name: whit_3,
        }

        return ret_val

    @staticmethod
    def __trinity(year: int) -> dict:
        """
        Calculates all dates related to Trinity.
        Trinity - Sundays between Whit and Advent.

        :param year: given year.
        :type year: int
        :return:  dictionary with ChurchYear enum's name as key and date as value.
        :rtype: dict
        """
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
                ret_val[key] = date

        return ret_val

    @staticmethod
    def __static_dates(year: int) -> dict:
        enums = list(map(lambda x: x.name, [
            ChurchYear.VISITATION,
            ChurchYear.REFORMATION,
            ChurchYear.CANDLEMAS,
            ChurchYear.ANNUNCIATION,
            ChurchYear.JOHN,
            ChurchYear.MICHAELMAS,
        ]))
        easter = calc_easter(year)
        annunciation = date_from_str(f'{year}-03-25')
        palm_sunday = easter - timedelta(weeks=1)
        if annunciation >= palm_sunday:
            annunciation = easter + timedelta(weeks=1) + timedelta(days=1)

        return {
            enums[0]: date_from_str(f'{year}-07-02'),
            enums[1]: date_from_str(f'{year}-10-31'),
            enums[2]: date_from_str(f'{year}-02-02'),
            enums[3]: annunciation,
            enums[4]: date_from_str(f'{year}-06-24'),
            enums[5]: date_from_str(f'{year}-09-29'),
        }



class LabelCalendarSeason(CalendarSeason, Enum):
    ADVENT = 'Advent', 'https://en.wikipedia.org/wiki/Advent'
    CHRISTMAS = 'Christmas', 'https://en.wikipedia.org/wiki/Christmas'
    NEW_YEAR = 'New Year', ''
    EPIPHANY = 'Epiphany', 'https://en.wikipedia.org/wiki/Epiphany_season'
    SHROVETIDE = 'Shrovetide', 'https://en.wikipedia.org/wiki/Shrovetide'
    HOLY_WEEK = 'Holy Week', 'https://en.wikipedia.org/wiki/Holy_Week'
    AFTER_EASTER = 'After Easter', ''
    WHIT = 'Whit', ''
    TRINITY = 'Trinity', '',
    STATIC = 'Static', ''


class LabelCalendarCycle(Enum):
    TEMPORAL = 'Temporal Cycle'
    SANCTORAL = 'Sanctoral Cycle'


def get_church_year_enum():
    # 'jak spocitat advent - objevuje se 30.11.'
    # 'nedele po Vanocich a po Novem roce?'
    # pylint: disable=line-too-long
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
            ('CHRISTMAS_4', ('Sunday after Christmas', 'https://en.wikipedia.org/wiki/Christmas_Sunday', [LabelCalendarSeason.CHRISTMAS.value, LabelCalendarCycle.TEMPORAL.value])),
            ('NEW_YEAR_1', ("New Year's Day", 'https://en.wikipedia.org/wiki/New_Year%27s_Day', [LabelCalendarSeason.NEW_YEAR.value, LabelCalendarCycle.TEMPORAL.value])),
            ('NEW_YEAR_2', ("New Year's Day I", 'https://en.wikipedia.org/wiki/New_Year%27s_Day', [LabelCalendarSeason.NEW_YEAR.value, LabelCalendarCycle.TEMPORAL.value]))]
        + generate_data_for_church_year_enum(
            7,
            'epiphany',
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
            ('EASTER_1', ('Easter', 'https://en.wikipedia.org/wiki/Easter', [LabelCalendarSeason.HOLY_WEEK.value, LabelCalendarCycle.TEMPORAL.value])),
            ('EASTER_2', ('Easter Monday', 'https://en.wikipedia.org/wiki/Easter', [LabelCalendarSeason.HOLY_WEEK.value, LabelCalendarCycle.TEMPORAL.value])),
            ('EASTER_3', ('Easter Tuesday', 'https://en.wikipedia.org/wiki/Easter', [LabelCalendarSeason.HOLY_WEEK.value, LabelCalendarCycle.TEMPORAL.value])),
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
        ) +
        [
            ('VISITATION', ('Visitation', 'https://en.wikipedia.org/wiki/Visitation_(Christianity)', [LabelCalendarSeason.STATIC.value])),
            ('REFORMATION', ('Reformation Day', 'https://en.wikipedia.org/wiki/Reformation_Day', [LabelCalendarSeason.STATIC.value])),
            ('CANDLEMAS', ('Candlemas', 'https://en.wikipedia.org/wiki/Candlemas', [LabelCalendarSeason.STATIC.value])), # 'https://en.wikipedia.org/wiki/Presentation_of_Jesus_at_the_Temple'
            ('ANNUNCIATION', ('Annunciation', 'https://en.wikipedia.org/wiki/Annunciation', [LabelCalendarSeason.STATIC.value])),
            ('JOHN', ('Nativity of Saint John the Baptist', 'https://en.wikipedia.org/wiki/Nativity_of_John_the_Baptist', [LabelCalendarSeason.STATIC.value])),
            ('MICHAELMAS', ('Michaelmas', 'https://en.wikipedia.org/wiki/Michaelmas', [LabelCalendarSeason.STATIC.value])),
        ],
        type=ChristianHoliday)

    return ret_val


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


def main():
    holidays = []
    for member in ChurchYear:
        member.ident = member.name
        holidays.append(member.dates_for_holiday(member, range(2022, 2023)))

    return pd.DataFrame([vars(t) for t in holidays]).loc[:, ['ident', 'title', 'url_link', 'labels', 'dates']]
