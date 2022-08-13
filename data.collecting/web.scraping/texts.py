import time

import pandas as pd
import logging
import helpers


def get_text_for(cantata):
    sp = helpers.make_request(f'https://webdocs.cs.ualberta.ca/~wfb/cantatas/{cantata}.html')
    movements = []
    instruments = []
    texts = []

    sp_table = sp.find_all('table')[0]

    for td in sp_table.find_all('td', class_='movement'):
        movements.append(td.find('b').text)
        instruments.append(td.find('em').text)

    for td in sp_table.find_all('td', class_='text'):
        texts.append(td.text)

    tmp_df = pd.DataFrame({'Movement': movements,
                           'Instruments': instruments,
                           'Text': texts,
                           'BWV': cantata})

    return tmp_df


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    df = pd.DataFrame()
    bwv = pd.read_csv("./_data/cantatas.csv", usecols=[0], header=None)[0].tolist()
    bwv = bwv[3:5]

    for item in bwv:
        try:
            tmp = get_text_for(item)
            df = pd.concat([df, tmp])
            logger.info(f'cantata processed {item}')
            time.sleep(5.0)
        except(Exception,):
            logger.error(f'error in cantata {item}')
            pass

    df.to_csv('./_data/texts.csv')
