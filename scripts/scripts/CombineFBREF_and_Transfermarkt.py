import numpy as np
import pandas as pd
import dataframeSaver


def combine():
    fbref = pd.read_excel('../data/FBREF.xlsx')
    tm = pd.read_excel('../data/transfermarkt.xlsx')
    # drop rows when there is no such player in both tables
    df = pd.merge(tm, fbref, on='Player', how='inner')
    dataframeSaver.saveDataframe(df, 'fbref_transfermarkt_dataset.xlsx')
