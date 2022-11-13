#pylint: disable=no-member
import pandas as pd
import christian_holidays as holidays

ChurchYear = holidays.get_church_year_enum()

cantatas = {
    ChurchYear.ADVENT_1: [36, 61, 62],
    ChurchYear.ADVENT_4: [132],
    ChurchYear.CHRISTMAS_1: [63, 91, 110, 191],
    ChurchYear.CHRISTMAS_2: [40, 57, 121],
    ChurchYear.CHRISTMAS_3: [64, 133, 151],
    ChurchYear.CHRISTMAS_4: [28, 122, 152],
    ChurchYear.NEW_YEAR_1: [16, 41, 143, 171, 190],
    ChurchYear.NEW_YEAR_2: [58, 153],
    ChurchYear.EPIPHANY_1: [65, 123],
    ChurchYear.EPIPHANY_2: [32, 124, 154],
    ChurchYear.EPIPHANY_3: [3, 13, 155],
    ChurchYear.EPIPHANY_4: [72, 73, 111, 156],
    ChurchYear.EPIPHANY_5: [14, 81],
    ChurchYear.SEPTUAGESIMA: [84, 92, 144],
    ChurchYear.SEXAGESIMA: [18, 126, 181],
    ChurchYear.QUINQUAGESIMA: [22, 23, 127, 159],
    ChurchYear.PALM_SUNDAY: [182],
    ChurchYear.EASTER_1: [4, 31],
    ChurchYear.EASTER_2: [6, 66],
    ChurchYear.EASTER_3: [134, 145, 158],
    ChurchYear.QUASIMODOGENITI: [42, 67],
    ChurchYear.MISERICORDIAS_DOMINI: [85, 104, 112],
    ChurchYear.JUBILATE: [12, 103, 146],
    ChurchYear.CANTATE: [108, 166],
    ChurchYear.ROGATE: [86, 87],
    ChurchYear.ASCENSION: [11, 37, 43, 128],
    ChurchYear.EXAUDI: [44, 183],
    ChurchYear.WHIT_1: [34, 59, 74, 172],
    ChurchYear.WHIT_2: [68, 173, 174],
    ChurchYear.WHIT_3: [175, 184],
    ChurchYear.TRINITY_1: [129, 165, 176, 194],
    ChurchYear.TRINITY_2: [20, 39, 75],
    ChurchYear.TRINITY_3: [2, 76],
    ChurchYear.TRINITY_4: [21, 135],
    ChurchYear.TRINITY_5: [24, 177, 185],
    ChurchYear.TRINITY_6: [88, 93],
    ChurchYear.TRINITY_7: [9, 170],
    ChurchYear.TRINITY_8: [54, 107, 186, 187],
    ChurchYear.TRINITY_9: [45, 136, 178],
    ChurchYear.TRINITY_10: [94, 105, 168],
    ChurchYear.TRINITY_11: [46, 101, 102],
    ChurchYear.TRINITY_12: [113, 179, 199],
    ChurchYear.TRINITY_13: [35, 137],
    ChurchYear.TRINITY_14: [33, 77, 164],
    ChurchYear.TRINITY_15: [17, 25, 78],
    ChurchYear.TRINITY_16: [51, 99, 138],
    ChurchYear.TRINITY_17: [8, 27, 95, 161],
    ChurchYear.TRINITY_18: [47, 114, 148],
    ChurchYear.TRINITY_19: [96, 169],
    ChurchYear.TRINITY_20: [5, 48, 56],
    ChurchYear.TRINITY_21: [49, 162, 180],
    ChurchYear.TRINITY_22: [38, 98, 109, 188],
    ChurchYear.TRINITY_23: [55, 89, 115],
    ChurchYear.TRINITY_24: [52, 139, 163],
    ChurchYear.TRINITY_25: [26, 60],
    ChurchYear.TRINITY_26: [90, 116],
    ChurchYear.TRINITY_27: [70],
    ChurchYear.TRINITY_28: [140],
    ChurchYear.VISITATION: [10, 147],
    ChurchYear.REFORMATION: [79, 80],
    ChurchYear.CANDLEMAS: [82, 83, 125],
    ChurchYear.ANNUNCIATION: [1],
    ChurchYear.JOHN: [7, 30, 167],
    ChurchYear.MICHAELMAS: [19, 50, 130, 149],
}


def main():
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)

    df_holidays = holidays.main()
    df_cantatas = pd.DataFrame([(key.name, value) for key, value in cantatas.items()], columns=['ident', 'bwv'])

    # print(df_holidays.dropna())
    df = pd.merge(left=df_holidays, right=df_cantatas, how='inner')
    print(df)

main()
