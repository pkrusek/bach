import re
from datetime import date
import bachcantatascom
from pprint import pprint

if __name__ == '__main__':
    df = bachcantatascom.get_main_table()
    pprint(df)
