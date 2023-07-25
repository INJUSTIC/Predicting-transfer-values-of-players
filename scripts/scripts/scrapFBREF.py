from functools import reduce
import pandas as pd
from cleaningFBREF import *
import dataframeSaver


def scrapFBREF():

    countries = ['england', 'france', 'germany', 'italy', 'spain']
    seasons = ['23', '22', '21']
    sheet_types = ['standard', 'shooting', 'goal_shot_creation',
                   'possession', 'passing', 'defensive_actions']

    data = {}
    colls = {}

    for country in countries:
        data[country] = {}
        for season in seasons:
            data[country][season] = {}
            for sheet_type in sheet_types:
                path = f'../data/{country}/{season}/{sheet_type}.xlsx'

                exls = pd.read_excel(path)

                if sheet_type not in colls:
                    colls[sheet_type] = exls.columns
                else:
                    exls.columns = colls[sheet_type]

                data[country][season][sheet_type] = exls

    clean_up_look_up = {'standard': lambda sheet: clean_std(clean_player_name(sheet.drop(['Rk', 'Nation', 'Pos', 'Age', 'Gls', 'Non-penalty xG', '90s', 'Born', 'Squad'], axis=1))),
                        'shooting': lambda sheet: clean_shooting(clean_player_name(sheet.drop(['Rk', 'Nation', 'Pos', 'Squad', 'Age', 'Born', '90s', 'Penalty Goals', 'Penalty Kicks Attempted', 'xG'], axis=1))),
                        'goal_shot_creation': lambda sheet: clean_goal_shot_creation(clean_player_name(sheet.drop(['Rk', 'Nation', 'Pos', 'Squad', 'Age', 'Born', '90s'], axis=1))),
                        'possession': lambda sheet: clean_possession(clean_player_name(sheet.drop(['Rk', 'Nation', 'Pos', 'Squad', 'Age', 'Born', '90s', 'Progressive Passes Received'], axis=1))),
                        'passing': lambda sheet: clean_passing(clean_player_name(sheet.drop(['Rk', 'Nation', 'Pos', 'Squad', 'Age', 'Born', '90s', 'Progressive Passes', 'Expected Assisted Goals', 'Ast'], axis=1))),
                        'defensive_actions': lambda sheet: clean_defending(clean_player_name(sheet.drop(['Rk', 'Nation', 'Pos', 'Squad', 'Age', 'Born', '90s'], axis=1)))}

    def concat_types(sheets, season):
        merged = reduce(lambda left, right: pd.merge(
            left, right, on='Player'), sheets)
        merged.columns = [
            a+f' ({int(season) - 1}/{season})' for a in merged.columns]
        merged.rename(
            columns={f"Player ({int(season) - 1}/{season})": "Player"}, inplace=True)
        return merged

    allData = {}

    for season in seasons:
        cleaned_data = []

        for type in sheet_types:
            concatenated_data = pd.concat(
                [data[country][season][type] for country in countries])
            cleaned_data.append(clean_up_look_up[type](concatenated_data))

        allData[season] = concat_types(cleaned_data, season)

    three_season = pd.merge(pd.merge(
        allData['23'], allData['22'], how='outer'), allData['21'], how='outer')
    three_season = three_season[~three_season.duplicated(
        'Player', keep='first')]

    dataframeSaver.saveDataframe(three_season, 'FBREF.xlsx')
