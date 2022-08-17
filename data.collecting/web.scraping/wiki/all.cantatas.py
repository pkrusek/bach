"""
A python module that scraped data about Bach's sacred cantatas from Wikipedia.
- Created by Pavel Krusek <pavelkrusek@icloud.com> on 01/08/2022.
"""

import requests as req
import re
from bs4 import BeautifulSoup as bs
import pandas as pd
from pprint import pprint
from enum import Enum
from slugify import slugify


def make_request(url):
    """
    Makes request to given endpoint and gets beautiful soup object.

    Parameters
    ----------
    url : string
        A url for request.

    Returns
    -------
    soup : BeautifulSoup
        BeautifulSoup object with the requested html.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    page = req.get(url, headers=headers)
    soup = bs(page.content, 'html.parser')

    return soup


def clean_cantatas(df):
    """
    Cleans given dataframe.

    Parameters
    ----------
    df : dataframe
        Dataframe to clean.

    Returns
    ----------
    df : Pandas dataframe
        Cleaned dataframe.
    """
    df = df.copy(deep=True)
    df['BWV'] = df['BWV'].apply(lambda x: re.sub('^0+\\s', '', str(x)))
    df = df[pd.to_numeric(df['BWV'], errors='coerce').notnull()]
    df['BWV'] = df['BWV'].str.lstrip('0')
    # only sacred ones (magic numbers)
    df['BWV'] = df['BWV'].astype(int)
    df = df[(df['BWV'] < 200) & (df['BWV'] != 198)]

    return df


def save_all_cantatas(save: bool = False):
    """
    Parses table with list of all cantatas, converts them to pandas, and exports data to CSV file.

    Parameters
    ----------
    save : bool
        Option to save the generated list to the csv file on disk.
    """
    # sp = make_request('https://de.wikipedia.org/wiki/Liste_der_Bachkantaten')
    sp = make_request('https://en.wikipedia.org/wiki/List_of_Bach_cantatas')
    sp_table = sp.find_all('table', class_='wikitable sortable')[0]
    df = pd.read_html(str(sp_table))[0]
    df = clean_cantatas(df)
    pprint(df.columns)
    # df = df.loc[:, ['BWV', 'Titel']]
    df = df.loc[:, ['BWV', 'Title', 'Occasion']]
    # df['slug'] = df.apply(lambda row: slugify('bwv-' + str(row[0])) + '-' + slugify(row[1]), axis=1)
    df.to_csv("../_data/cantatas.csv", header=False, index=False)
    return df
    # df.to_csv("../_data/cantatas.csv", header=False, index=False) if save else pprint(df)


def get_all_sources():
    """
    Gets all html sources to cantata details from the table with all cantatas.

    Returns
    ----------
    df : Pandas dataframe
        List with dictionary with BWV numbers and html sources to the specific wiki pages.
    """
    sp = make_request('https://en.wikipedia.org/wiki/List_of_Bach_cantatas')
    sp_table = sp.find_all('table', class_='wikitable sortable')[0]
    sp_trs = sp_table.findChildren(['tr'])
    links = []
    for tr in sp_trs:
        link = tr.select_one(':nth-child(2)').select_one('a')
        if link is not None:
            data = {
                "BWV": re.sub('^0+\\s', '', tr.select_one(':nth-child(1)').text),
                "link": 'https://en.wikipedia.org' + link['href']
            }
            links.append(data)
    # for testing purposes
    links = links[0:5]
    pprint(links)
    df = pd.DataFrame(links)
    df = clean_cantatas(df)

    sp_sources = []
    for row in df.itertuples():
        sp = make_request(row[2])
        sp_sources.append(sp)

    df['source'] = sp_sources

    return df


def get_all_pages():
    df = get_all_sources()

    main_images = []
    movements = []
    for row in df.itertuples():
        main_images.append(get_main_image_for_cantata(row[3]))
        movements.append(get_movements(row[3], row[1]))

    result = pd.concat(movements)
    result = result.loc[:, ['BWV', 'Title']]
    result.to_csv("../_data/movements.csv", header=True, index=False)


def get_main_image_for_cantata(sp):
    """
    Gets main image and image caption, if exists. Otherwise, empty string/s.

    Parameters
    ----------
    sp : soup
        Html source for cantata.

    Returns
    ----------
    data : tuple
        Tuple with URL to image and caption.
    """
    main_image_url = ''
    main_caption = ''
    try:
        main_image_url = sp.find_all('td', class_='infobox-image')[0].findChildren("img")[0]['src']
    except(Exception,):
        pass
    try:
        main_caption = sp.find_all('div', class_='infobox-caption')[0].text
    except(Exception,):
        pass

    data = main_image_url, main_caption

    return data


def get_movements(sp, bwv):
    df = pd.DataFrame()
    try:
        table = sp.find_all(text=re.compile('Movements of'))[0].findParent('table')
        df = pd.read_html(str(table))[0]
        df['BWV'] = bwv
    except(Exception,):
        pprint('missing:')
        pprint(bwv)
        pass

    return df


def main():
    # df = save_all_cantatas()
    # get_all_pages()
    # save_all_cantatas()


if __name__ == '__main__':
    main()
