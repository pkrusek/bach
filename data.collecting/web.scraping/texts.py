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
        if td.previous_sibling.previous_sibling is not None:
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

    # only sacred ones
    bwv = list(range(1, 200))
    bwv.remove(198)
    # for testing purposes
    # bwv = bwv[3:5]

    for bwv_number in bwv:
        try:
            tmp = get_text_for(bwv_number)
            df = pd.concat([df, tmp])
            # The server doesn't like fast requests
            time.sleep(3.0)
        except(Exception,):
            logger.error(f'error in cantata {bwv_number}')
            pass

    df.to_csv('./_data/texts.csv')
