from pprint import pprint
from datetime import datetime, timedelta
import enum
import helpers
import warnings
import pandas as pd
import numpy as np
import re
import logging
from bs4 import BeautifulSoup as bs
import time


class InstrumentGroup(enum.Enum):
    solo = 'Solo'
    choir = 'Choir'
    brass = 'Brass and Percussion'
    wood = 'Woodwinds'
    strings = 'Strings'
    keyboard = 'Keyboard'
    bc = 'Continuo'


class Instrument(enum.Enum):
    tr = {'title': 'Tromba (trumpet)', 'links': ['https://en.wikipedia.org/wiki/Trumpet'],
          'group': InstrumentGroup.brass.name}
    tt = {'title': 'Tomba da tirarsi', 'links': ['https://en.wikipedia.org/wiki/Tromba_da_tirarsi'],
          'group': InstrumentGroup.brass.name}
    cl = {'title': 'Clarino (high Baroque trumpet)', 'links': ['https://en.wikipedia.org/wiki/Clarion_(instrument)'],
          'group': InstrumentGroup.brass.name}
    tb = {'title': 'Trombone', 'links': ['https://en.wikipedia.org/wiki/Trombone'], 'group': InstrumentGroup.brass.name}
    co = {'title': 'Corno (horn)', 'links': ['https://en.wikipedia.org/wiki/Natural_horn'],
          'group': InstrumentGroup.brass.name}
    cc = {'title': 'Corno da caccia', 'links': ['https://en.wikipedia.org/wiki/Corno_da_caccia'],
          'group': InstrumentGroup.brass.name}
    ct = {'title': 'Corno da tirarsi', 'links': ['https://en.wikipedia.org/wiki/Corno_da_tirarsi'],
          'group': InstrumentGroup.brass.name}
    li = {'title': 'Lituo (lituus)', 'links': ['https://en.wikipedia.org/wiki/Medieval_lituus'],
          'group': InstrumentGroup.brass.name}
    cn = {'title': 'Cornetto', 'links': ['https://en.wikipedia.org/wiki/Cornett'], 'group': InstrumentGroup.brass.name}
    ti = {'title': 'Timpani', 'links': ['https://en.wikipedia.org/wiki/Timpani'], 'group': InstrumentGroup.brass.name}
    fl = {'title': 'Flauto (recorder)', 'links': ['https://en.wikipedia.org/wiki/Recorder_(musical_instrument)'],
          'group': InstrumentGroup.wood.name}
    fp = {'title': 'Flauto piccolo', 'links': ['https://en.wikipedia.org/wiki/Flauto_piccolo'],
          'group': InstrumentGroup.wood.name}
    ft = {'title': 'Flauto traverso', 'links': ['https://en.wikipedia.org/wiki/Flauto_traverso'],
          'group': InstrumentGroup.wood.name}
    ob = {'title': 'Oboe', 'links': ['https://en.wikipedia.org/wiki/Oboe'], 'group': InstrumentGroup.wood.name}
    oa = {'title': "Oboe d'amore", 'links': ['https://en.wikipedia.org/wiki/Oboe_d%27amore'],
          'group': InstrumentGroup.wood.name}
    ot = {'title': 'Taille (tenor oboe)',
          'links': ['https://en.wikipedia.org/wiki/Taille_(instrument)', 'https://en.wikipedia.org/wiki/Oboe'],
          'group': InstrumentGroup.wood.name}
    oc = {'title': 'Oboe da caccia', 'links': ['https://en.wikipedia.org/wiki/Oboe_da_caccia'],
          'group': InstrumentGroup.wood.name}
    fg = {'title': 'Bassoon', 'links': ['https://en.wikipedia.org/wiki/Bassoon'], 'group': InstrumentGroup.wood.name}
    vl = {'title': 'Violino (violin)', 'links': ['https://en.wikipedia.org/wiki/Violin'],
          'group': InstrumentGroup.strings.name}
    vs = {'title': 'Violino solo', 'links': [''], 'group': InstrumentGroup.strings.name}
    va = {'title': 'Viola', 'links': ['https://en.wikipedia.org/wiki/Viola'], 'group': InstrumentGroup.strings.name}
    vc = {'title': 'Violoncello', 'links': ['https://en.wikipedia.org/wiki/Violoncello'],
          'group': InstrumentGroup.strings.name}
    vp = {'title': 'Violoncello piccolo', 'links': ['https://en.wikipedia.org/wiki/Violoncello_piccolo'],
          'group': InstrumentGroup.strings.name}
    vm = {'title': "Viola d'amore", 'links': ['https://en.wikipedia.org/wiki/Viola_d%27amore'],
          'group': InstrumentGroup.strings.name}
    vg = {'title': 'Viola da gamba', 'links': ['https://en.wikipedia.org/wiki/Viola_da_gamba'],
          'group': InstrumentGroup.strings.name}
    vt = {'title': 'Violetta', 'links': ['https://en.wikipedia.org/wiki/Violetta_(instrument)'],
          'group': InstrumentGroup.strings.name}
    vn = {'title': 'Violone', 'links': ['https://en.wikipedia.org/wiki/Violone'], 'group': InstrumentGroup.strings.name}
    org = {'title': 'Organo (organ)', 'links': ['https://en.wikipedia.org/wiki/Organ_(music)'],
           'group': InstrumentGroup.keyboard.name}
    cemb = {'title': 'Cembalo (harpsichord)', 'links': ['https://en.wikipedia.org/wiki/Harpsichord'],
            'group': InstrumentGroup.keyboard.name}
    lt = {'title': 'Liuto (lute)', 'links': ['https://en.wikipedia.org/wiki/Lute'],
          'group': InstrumentGroup.keyboard.name}
    bc = {'title': 'Basso continuo', 'links': ['https://en.wikipedia.org/wiki/Basso_continuo'],
          'group': InstrumentGroup.bc.name}

    xx = {'title': '', 'links': ['']}


def get_instruments_for_cantatas():
    """
    Parses table with list of all cantatas, converts them to pandas, and exports data to CSV file.

    Parameters
    ----------
    save : bool
        Option to save the generated list to the csv file on disk.
    """
    sp = helpers.make_request('https://en.wikipedia.org/wiki/List_of_Bach_cantatas')
    sp_table = sp.find_all('table', class_='wikitable sortable')[0]
    # pprint(sp_table)
    df = pd.read_html(str(sp_table))[0]
    df = helpers.clean_cantatas(df)
    df = df.loc[:, ['BWV', 'Solo', 'Choir', 'Brass', 'Wood', 'Strings', 'Key', 'Bc']]
    # df.Brass = df.Brass.str.lower()
    # df.Wood = df.Wood.str.lower()
    # df.Strings = df.Strings.str.lower()
    return df


def process_instrument_group(instrument):
    global df_cantatas
    global df
    df[instrument] = df[instrument].str.lower()
    in_df = df[df[instrument].notnull()][['BWV', instrument]]
    for row in in_df.itertuples():
        tmp = pd.DataFrame({'BWV': row[1], 'Instrument': row[2].split(' ')})
        tmp.Instrument = tmp.Instrument.str.replace('[()]', '', regex=True)
        tmp['Quantity'] = tmp.Instrument.str.extract(r'(^\d+)')
        tmp.Instrument = tmp.Instrument.str.replace(r'(^\d+)', '', regex=True)
        df_cantatas = pd.concat([df_cantatas, tmp])


def get_movements(sp, bwv):
    ret_df = pd.DataFrame()
    try:
        sp = bs(sp, "html.parser")
        table = sp.find_all(text=re.compile('Movements of'))[0].findParent('table')
        pprint(sp.find_all(text=re.compile('Movements of')))
        ret_df = pd.read_html(str(table))[0]
        ret_df['BWV'] = bwv
    except Exception as e:
        # logger.error(f'error in cantata {bwv} with error {str(e)}')
        pass

    return ret_df


def get_movement_source_for(cantata):
    global df_movement_sources
    try:
        sp = helpers.make_request(f'https://bach-cantatas.com/INS/{cantata}')
        tmp = pd.DataFrame(columns=['BWV','Source'])
        tmp.loc[0] = [cantata, sp]
        df_movement_sources = pd.concat([df_movement_sources, tmp])

        next_mvt = sp.find(text=re.compile('Next Mvt')).findParent('a')
        if next_mvt is None:
            pprint(f'cantata {cantata} done')
            df_movement_sources.to_csv("./_data/movements_sources.csv")
            time.sleep(1.5)
            get_movements_sources(cantata)
        else:
            pprint(f'cantata {cantata} done')
            time.sleep(1.5)
            get_movement_source_for(next_mvt['href'])
    except Exception as e:
        logger.error(f'error in source - cantata {cantata} with error {str(e)}')
        get_movements_sources(cantata)


def get_movements_sources(cantata):
    # 'BWV015-01.htm'
    # 'BWV082-01.htm'
    # 'BWV118-01.htm'
    # '127, 128'
    cantata = re.sub('-.*htm', '-01.htm', cantata)
    bwv = list(range(1, 200))
    bwv.remove(198)
    bwv = list(map(lambda x: f'BWV{str(x).zfill(3)}-01.htm', bwv))
    try:
        indx = bwv.index(cantata)
        if indx + 1 < len(bwv):
            next_cantata = bwv[indx + 1]
            get_movement_source_for(next_cantata)
    except Exception as e:
        logger.error(f'error in sources - cantata {cantata} with error {str(e)}')


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    df_movement_sources = pd.DataFrame()

    get_movement_source_for('BWV001-01.htm')
    # df = pd.read_csv('./_data/movements_sources.csv')
    # pprint(df)

    # df_cantatas = pd.DataFrame()
    # df = get_instruments_for_cantatas()
    #
    # process_instrument_group('Brass')
    # process_instrument_group('Wood')
    # process_instrument_group('Brass')
    # process_instrument_group('Bc')
    # process_instrument_group('Key')

    # df_sources = helpers.get_all_sources('https://en.wikipedia.org/wiki/List_of_Bach_cantatas')
    # res = [get_movements(x, y) for x, y in zip(df_sources['source'], df_sources['BWV'])]
    # pprint(res)

    # pprint(df_cantatas.head(36))
