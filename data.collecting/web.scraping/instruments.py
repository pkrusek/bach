from pprint import pprint
from datetime import datetime, timedelta
import enum
import helpers
import warnings
import pandas as pd
import numpy as np
import re


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
    df = clean_cantatas(df)
    df = df.loc[:, ['BWV', 'Solo', 'Choir', 'Brass', 'Wood', 'Strings', 'Key', 'Bc']]
    df.Brass = df.Brass.str.lower()
    df.Wood = df.Wood.str.lower()
    df.Strings = df.Strings.str.lower()
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


if __name__ == '__main__':
    df_cantatas = pd.DataFrame()
    df = get_instruments_for_cantatas()

    process_instrument_group('Brass')
    process_instrument_group('Wood')
    process_instrument_group('Brass')
    process_instrument_group('Bc')
    process_instrument_group('Key')

    pprint(df_cantatas.head(36))
