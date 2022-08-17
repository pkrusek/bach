import re
from datetime import date


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def test_regexp():
    # Spotify search
    test = 'Christ lag in Todes Banden, BWV 4: Versus IV: Es war ein wunderlicher Krieg'
    what = 'bwv 4'
    regexp = re.compile('(?i)%s(?![0-9])' % what)
    if regexp.search(test):
        print('matched')


def test_regexp2():
    # Leading zeros
    test = '00 4'
    res = re.sub('^0+\\s', '', test)
    print(res)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start_interval = 1950
    end_interval = 2042
    for year in range(start_interval, end_interval):
        easter = calc_easter(year)
        print(easter.strftime('%Y-%m-%d'))
