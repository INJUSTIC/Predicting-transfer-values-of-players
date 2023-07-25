import numpy as np
import pandas as pd
from pandas import DataFrame
import math
import dataframeSaver


def dropGoalkeepers():
    df = pd.read_excel('../data/fbref_transfermarkt_dataset.xlsx')
    df = df[df['Position'] != 'Goalkeeper']
    df.reset_index(drop=True, inplace=True)
    return df


def get_mean_float_values(*values):
    float_values = [value for value in values if isinstance(value, float)]
    return round(np.mean(float_values), 2)


def fill_na(filledDataset, firstFillDataset, secFillDataset):
    for a in list(range(len(filledDataset))):
        for b in list(range(len(filledDataset.columns))):
            if math.isnan(filledDataset.iloc[a, b]):
                value_first = firstFillDataset.iloc[a][b]
                value_sec = secFillDataset.iloc[a][b]
                if not math.isnan(value_first) and not math.isnan(value_sec):
                    filledDataset.iloc[a][b] = get_mean_float_values(
                        value_first, value_sec)
                elif not math.isnan(value_first):
                    filledDataset.iloc[a][b] = value_first
                else:
                    filledDataset.iloc[a][b] = value_sec


def avg_missing(df: DataFrame):
    df23 = df.iloc[:, 9:122]
    df22 = df.iloc[:, 122:235]
    df21 = df.iloc[:, 235:348]
    fill_na(df23, df22, df21)
    fill_na(df22, df23, df21)
    fill_na(df21, df22, df23)

    df_tm = df.iloc[:, :9]
    final = pd.concat([df_tm, df23, df22, df21], axis=1)

    final = final.dropna()

    final.reset_index(drop=True, inplace=True)
    dataframeSaver.saveDataframe(final, 'final_dataset.xlsx')
