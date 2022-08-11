import requests as req
from bs4 import BeautifulSoup as bs
from datetime import date, datetime, timedelta


def get_easter(year):
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


def get_last_weekday(in_date, weekday):
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


def get_next_weekday(in_date, weekday):
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


def get_date_from_str(in_str):
    """
    Converts given date string in format 'YYYY.MM.DD' to date object.

    :param in_str: str
    :return: date
    """
    return datetime.strptime(in_str, '%Y-%m-%d')


def make_request(url):
    """
    Makes request to given endpoint and gets beautiful soup object.

    :param: url: string
        A url for request.

    :return: BeautifulSoup
        A object with the requested html.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    page = req.get(url, headers=headers)
    sp = bs(page.content, 'html.parser')

    return sp
