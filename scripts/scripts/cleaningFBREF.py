from datetime import datetime
import numpy as np
import pandas as pd


def clean_player_name(df):
    
    special_char = ['\xad','À','Á','Ç','É','Ñ','Ó','Ö','Ø','Ü','ß',
                     'à','á','â','ã','ä','å','æ','ç','è','é','ê','ë',
                     'í','î','ï','ð','ñ','ò','ó','ô','ö','ø','ú','ü',
                     'ý','ă','ą','Ć','ć','Č','č','Đ','đ','ę','ě','ğ',
                     'İ','ı','ľ','Ł','ł','ń','ň','ō','ř','Ş','ş','Š',
                     'š','ů','Ž','ž','Ș','ș','ț']

    replacement = ['','A','A','C','E','N','O','O','O','U','ss',
                    'a','a','a','a','a','a','ae','c','e','e','e',
                    'e','i','i','i','d','n','o','o','o','o','o',
                    'u','u','y','a','a','C','c','C','c','D','d',
                    'e','e','g','I','i','l','L','l','n','n','o',
                    'r','S','s','S','s','u','Z','z','S','s','t']

    clean_players = []
    for name in df['Player']:
        clean_string = []
        for symb in name:
            if symb in special_char:
                for i in range(0, len(special_char)):
                    if symb == special_char[i]:
                        clean_string.append(replacement[i])
            else:
                clean_string.append(symb)
        clean_string = ''.join(clean_string)
        clean_players.append(clean_string)



    df['Player'] = clean_players 
    return df

def convertDateToFloat(date):
    splittedStr = str(date).split(' ')[0].split('-')[1:]
    intPart = int(splittedStr[1])
    decPart = int(splittedStr[0])
    res = intPart + decPart/10
    return res

def fixDataframe(df):
    for index, row in df.iterrows():
        for column in df.columns:
            cell_value = df.at[index, column]
            if isinstance(cell_value, datetime):
                df.at[index, column] = convertDateToFloat(cell_value)
            elif column != 'Player' and isinstance(cell_value, str):
                df.at[index, column] = float(cell_value)
    return df
                

def clean_std(dataframe: pd.DataFrame):
    #print(len(dataframe))
    dataframe.reset_index(drop=True, inplace=True)
    fixDataframe(dataframe)
    duplicates = pd.DataFrame(columns=dataframe.columns)
    duplicated_rows = dataframe[dataframe.duplicated(subset='Player', keep=False)]
    duplicates = duplicates.append(duplicated_rows)
    dataframe = dataframe.drop_duplicates(subset='Player', keep=False)
    dataframe.reset_index(drop=True, inplace=True)
    duplicates.reset_index(drop=True, inplace=True)
    duplicates = duplicates.sort_values(by='Player')
    transferred_players_list = []
    for i in range(0, len(duplicates), 2):
        if i+1 < len(duplicates):
            transferred_player_combine = pd.Series([duplicates.iloc[i]['Player'],
                            duplicates.iloc[i]['MP']+duplicates.iloc[i+1]['MP'],
                            duplicates.iloc[i]['Starts']+duplicates.iloc[i+1]['Starts'],
                            duplicates.iloc[i]['Min']+duplicates.iloc[i+1]['Min'],
                            duplicates.iloc[i]['Ast']+duplicates.iloc[i+1]['Ast'],
                            duplicates.iloc[i]['G+A']+duplicates.iloc[i+1]['G+A'],
                            duplicates.iloc[i]['Non-penalty Goals']+duplicates.iloc[i+1]['Non-penalty Goals'],
                            duplicates.iloc[i]['Penalty Goals']+duplicates.iloc[i+1]['Penalty Goals'],
                            duplicates.iloc[i]['Penalty Kicks Attempted']+duplicates.iloc[i+1]['Penalty Kicks Attempted'],
                            duplicates.iloc[i]['CrdY']+duplicates.iloc[i+1]['CrdY'],
                            duplicates.iloc[i]['CrdR']+duplicates.iloc[i+1]['CrdR'],
                            duplicates.iloc[i]['xG']+duplicates.iloc[i+1]['xG'],
                            duplicates.iloc[i]['Expected Assisted Goals']+duplicates.iloc[i+1]['Expected Assisted Goals'],
                            duplicates.iloc[i]['Non-penalty xG Plus Assisted Goals']+duplicates.iloc[i+1]['Non-penalty xG Plus Assisted Goals'],
                            duplicates.iloc[i]['Progressive Carries']+duplicates.iloc[i+1]['Progressive Carries'],
                            duplicates.iloc[i]['Progressive Passes']+duplicates.iloc[i+1]['Progressive Passes'],
                            duplicates.iloc[i]['Progressive Passes Received']+duplicates.iloc[i+1]['Progressive Passes Received'],
                            duplicates.iloc[i]['Gls/90']+duplicates.iloc[i+1]['Gls/90'],
                            duplicates.iloc[i]['Ast/90']+duplicates.iloc[i+1]['Ast/90'],
                            duplicates.iloc[i]['(G+A)/90']+duplicates.iloc[i+1]['(G+A)/90'],
                            duplicates.iloc[i]['Non-penalty Goals/90']+duplicates.iloc[i+1]['Non-penalty Goals/90'],
                            duplicates.iloc[i]['Non-penalty Goals + Assists/90']+duplicates.iloc[i+1]['Non-penalty Goals + Assists/90'],
                            duplicates.iloc[i]['xG/90']+duplicates.iloc[i+1]['xG/90'],
                            duplicates.iloc[i]['Expected Assisted Goals/90']+duplicates.iloc[i+1]['Expected Assisted Goals/90'],
                            duplicates.iloc[i]['xG Plus Assisted Goals/90']+duplicates.iloc[i+1]['xG Plus Assisted Goals/90'],
                            duplicates.iloc[i]['Non-penalty xG/90']+duplicates.iloc[i+1]['Non-penalty xG/90'],
                            duplicates.iloc[i]['Non-penalty xG Plus Assisted Goals/90']+duplicates.iloc[i+1]['Non-penalty xG Plus Assisted Goals/90']])

        transferred_players_list.append(transferred_player_combine)

    transferred_players = pd.DataFrame(transferred_players_list)
    transferred_players.columns = dataframe.columns
    final_df = pd.concat([dataframe, transferred_players])
    final_df = final_df.reset_index(drop=True)
    return final_df
    
    
    
def clean_shooting(dataframe):

    dataframe.reset_index(drop=True, inplace=True)
    fixDataframe(dataframe)
    duplicates = pd.DataFrame(columns=dataframe.columns)
    duplicated_rows = dataframe[dataframe.duplicated(subset='Player', keep=False)]
    duplicates = duplicates.append(duplicated_rows)
    dataframe = dataframe.drop_duplicates(subset='Player', keep=False)
    dataframe.reset_index(drop=True, inplace=True)
    duplicates.reset_index(drop=True, inplace=True)
    duplicates = duplicates.sort_values(by='Player')

    transferred_players_list = []

    for i in range(0, len(duplicates), 2):
        if i+1 < len(duplicates):
            if (duplicates.iloc[i]['Shots'] + duplicates.iloc[i+1]['Shots']) == 0 or (duplicates.iloc[i]['Shots On Target'] + duplicates.iloc[i+1]['Shots On Target']) == 0:

                transferred_player_combine = pd.Series([duplicates.iloc[i]['Player'],
                                            duplicates.iloc[i]['Gls']+duplicates.iloc[i+1]['Gls'],
                                            duplicates.iloc[i]['Shots']+duplicates.iloc[i+1]['Shots'],
                                            duplicates.iloc[i]['Shots On Target']+duplicates.iloc[i+1]['Shots On Target'],
                                            0,
                                            duplicates.iloc[i]['Shots/90']+duplicates.iloc[i+1]['Shots/90'],
                                            duplicates.iloc[i]['Shots On Target/90']+duplicates.iloc[i+1]['Shots On Target/90'],
                                            0,
                                            0,
                                            (duplicates.iloc[i]['Dist']+duplicates.iloc[i+1]['Dist'])/2,
                                            duplicates.iloc[i]['Shots From Free Kicks']+duplicates.iloc[i+1]['Shots From Free Kicks'],
                                            duplicates.iloc[i]['Non-penalty xG']+duplicates.iloc[i+1]['Non-penalty xG'],
                                            0,
                                            duplicates.iloc[i]['Goals Minus xG']+duplicates.iloc[i+1]['Goals Minus xG'],
                                            duplicates.iloc[i]['Non-penalty Goals Minus Non-penalty xG']+duplicates.iloc[i+1]['Non-penalty Goals Minus Non-penalty xG']])
            else:
                transferred_player_combine = pd.Series([duplicates.iloc[i]['Player'],
                                            duplicates.iloc[i]['Gls']+duplicates.iloc[i+1]['Gls'],
                                            duplicates.iloc[i]['Shots']+duplicates.iloc[i+1]['Shots'],
                                            duplicates.iloc[i]['Shots On Target']+duplicates.iloc[i+1]['Shots On Target'],
                                            (duplicates.iloc[i]['Shots On Target']+duplicates.iloc[i+1]['Shots On Target'])/(duplicates.iloc[i]['Shots'] + duplicates.iloc[i+1]['Shots'])*100,
                                            duplicates.iloc[i]['Shots/90']+duplicates.iloc[i+1]['Shots/90'],
                                            duplicates.iloc[i]['Shots On Target/90']+duplicates.iloc[i+1]['Shots On Target/90'],
                                            (duplicates.iloc[i]['Gls']+duplicates.iloc[i+1]['Gls'])/(duplicates.iloc[i]['Shots']+duplicates.iloc[i+1]['Shots']),
                                            (duplicates.iloc[i]['Gls']+duplicates.iloc[i+1]['Gls'])/(duplicates.iloc[i]['Shots On Target']+duplicates.iloc[i+1]['Shots On Target']),
                                            (duplicates.iloc[i]['Dist']+duplicates.iloc[i+1]['Dist'])/2,
                                            duplicates.iloc[i]['Shots From Free Kicks']+duplicates.iloc[i+1]['Shots From Free Kicks'],
                                            duplicates.iloc[i]['Non-penalty xG']+duplicates.iloc[i+1]['Non-penalty xG'],
                                            (duplicates.iloc[i]['Non-penalty xG']+duplicates.iloc[i+1]['Non-penalty xG'])/(duplicates.iloc[i]['Shots']+duplicates.iloc[i+1]['Shots']),
                                            duplicates.iloc[i]['Goals Minus xG']+duplicates.iloc[i+1]['Goals Minus xG'],
                                            duplicates.iloc[i]['Non-penalty Goals Minus Non-penalty xG']+duplicates.iloc[i+1]['Non-penalty Goals Minus Non-penalty xG']])

        transferred_players_list.append(transferred_player_combine)
    
    transferred_players = pd.DataFrame(transferred_players_list)
    transferred_players.columns = dataframe.columns
    final_df = pd.concat([dataframe, transferred_players])
    final_df = final_df.reset_index(drop=True)
    return final_df
    
    
    
def clean_goal_shot_creation(dataframe):

    dataframe.reset_index(drop=True, inplace=True)
    fixDataframe(dataframe)
    duplicates = pd.DataFrame(columns=dataframe.columns)
    duplicated_rows = dataframe[dataframe.duplicated(subset='Player', keep=False)]
    duplicates = duplicates.append(duplicated_rows)
    dataframe = dataframe.drop_duplicates(subset='Player', keep=False)
    dataframe.reset_index(drop=True, inplace=True)
    duplicates.reset_index(drop=True, inplace=True)
    duplicates = duplicates.sort_values(by='Player')

    transferred_players_list = []

    for i in range(0, len(duplicates), 2):
        if i+1 < len(duplicates):
            transferred_player_combine = pd.Series([duplicates.iloc[i]['Player'],
                                            duplicates.iloc[i]['Shot Creating Actions'] + duplicates.iloc[i+1]['Shot Creating Actions'],
                                            duplicates.iloc[i]['Shot Creating Actions/90'] + duplicates.iloc[i+1]['Shot Creating Actions/90'],
                                            duplicates.iloc[i]['PassLive Shot'] + duplicates.iloc[i+1]['PassLive Shot'],
                                            duplicates.iloc[i]['PassDead Shot'] + duplicates.iloc[i+1]['PassDead Shot'],
                                            duplicates.iloc[i]['Take-ons Shot'] + duplicates.iloc[i+1]['Take-ons Shot'],
                                            duplicates.iloc[i]['Shots That Lead To Another Shot Attempt'] + duplicates.iloc[i+1]['Shots That Lead To Another Shot Attempt'],
                                            duplicates.iloc[i]['Fouls drawn That Lead To A Shot Attempt'] + duplicates.iloc[i+1]['Fouls drawn That Lead To A Shot Attempt'],
                                            duplicates.iloc[i]['Defensive Actions That Lead To A Shot Attempt'] + duplicates.iloc[i+1]['Defensive Actions That Lead To A Shot Attempt'],
                                            duplicates.iloc[i]['Goal-creating Actions'] + duplicates.iloc[i+1]['Goal-creating Actions'],
                                            duplicates.iloc[i]['Goal-creating Actions/90'] + duplicates.iloc[i+1]['Goal-creating Actions/90'],
                                            duplicates.iloc[i]['PassLive Goal'] + duplicates.iloc[i+1]['PassLive Goal'],
                                            duplicates.iloc[i]['PassDead Goal'] + duplicates.iloc[i+1]['PassDead Goal'],
                                            duplicates.iloc[i]['Take-ons Goal'] + duplicates.iloc[i+1]['Take-ons Goal'],
                                            duplicates.iloc[i]['Shots That Lead To Another Goal-scoring Shot'] + duplicates.iloc[i+1]['Shots That Lead To Another Goal-scoring Shot'],
                                            duplicates.iloc[i]['Fouls drawn That Lead To A Goal'] + duplicates.iloc[i+1]['Fouls drawn That Lead To A Goal'],
                                            duplicates.iloc[i]['Defensive Actions That Lead To A Goal'] + duplicates.iloc[i+1]['Defensive Actions That Lead To A Goal']])


        transferred_players_list.append(transferred_player_combine)

    transferred_players = pd.DataFrame(transferred_players_list)
    transferred_players.columns = dataframe.columns
    final_df = pd.concat([dataframe, transferred_players])
    final_df = final_df.reset_index(drop=True)
    return final_df

    
    
    
    
    
def clean_possession(dataframe):

    dataframe.reset_index(drop=True, inplace=True)
    fixDataframe(dataframe)
    duplicates = pd.DataFrame(columns=dataframe.columns)
    duplicated_rows = dataframe[dataframe.duplicated(subset='Player', keep=False)]
    duplicates = duplicates.append(duplicated_rows)
    dataframe = dataframe.drop_duplicates(subset='Player', keep=False)
    dataframe.reset_index(drop=True, inplace=True)
    duplicates.reset_index(drop=True, inplace=True)
    duplicates = duplicates.sort_values(by='Player')

    transferred_players_list = []

    for i in range(0, len(duplicates), 2):
        if i+1 < len(duplicates):
            if (duplicates.iloc[i]['Total Attempted Dribbles'] + duplicates.iloc[i+1]['Total Attempted Dribbles']) == 0:
            
            
                transferred_player_combine = pd.Series([duplicates.iloc[i]['Player'],
                                                    duplicates.iloc[i]['Touches']+duplicates.iloc[i+1]['Touches'],
                                                    duplicates.iloc[i]['Touches In Def Pen Area']+duplicates.iloc[i+1]['Touches In Def Pen Area'],
                                                    duplicates.iloc[i]['Touches in Defensive 3rd']+duplicates.iloc[i+1]['Touches in Defensive 3rd'],
                                                    duplicates.iloc[i]['Touches in Midfield 3rd']+duplicates.iloc[i+1]['Touches in Midfield 3rd'],
                                                    duplicates.iloc[i]['Touches in Attacking 3rd']+duplicates.iloc[i+1]['Touches in Attacking 3rd'],
                                                    duplicates.iloc[i]['Touches in Attacking Penalty Box']+duplicates.iloc[i+1]['Touches in Attacking Penalty Box'],
                                                    duplicates.iloc[i]['Touches in Open-play']+duplicates.iloc[i+1]['Touches in Open-play'],
                                                    0,
                                                    0,
                                                    0,
                                                    0,
                                                    0,
                                                    duplicates.iloc[i]['Carries']+duplicates.iloc[i+1]['Carries'],
                                                    duplicates.iloc[i]['Total Carrying Distance']+duplicates.iloc[i+1]['Total Carrying Distance'],
                                                    duplicates.iloc[i]['Progressive Carrying Distance']+duplicates.iloc[i+1]['Progressive Carrying Distance'],
                                                    duplicates.iloc[i]['Progressive Carries']+duplicates.iloc[i+1]['Progressive Carries'],
                                                    duplicates.iloc[i]['Carries Into Final Third']+duplicates.iloc[i+1]['Carries Into Final Third'],
                                                    duplicates.iloc[i]['Carries Into Penalty Area']+duplicates.iloc[i+1]['Carries Into Penalty Area'],
                                                    duplicates.iloc[i]['Miscontrols']+duplicates.iloc[i+1]['Miscontrols'],
                                                    duplicates.iloc[i]['Dispossessed']+duplicates.iloc[i+1]['Dispossessed'],
                                                    duplicates.iloc[i]['Passes Received']+duplicates.iloc[i+1]['Passes Received']])
            else:
                    transferred_player_combine = pd.Series([duplicates.iloc[i]['Player'],
                                                    duplicates.iloc[i]['Touches']+duplicates.iloc[i+1]['Touches'],
                                                    duplicates.iloc[i]['Touches In Def Pen Area']+duplicates.iloc[i+1]['Touches In Def Pen Area'],
                                                    duplicates.iloc[i]['Touches in Defensive 3rd']+duplicates.iloc[i+1]['Touches in Defensive 3rd'],
                                                    duplicates.iloc[i]['Touches in Midfield 3rd']+duplicates.iloc[i+1]['Touches in Midfield 3rd'],
                                                    duplicates.iloc[i]['Touches in Attacking 3rd']+duplicates.iloc[i+1]['Touches in Attacking 3rd'],
                                                    duplicates.iloc[i]['Touches in Attacking Penalty Box']+duplicates.iloc[i+1]['Touches in Attacking Penalty Box'],
                                                    duplicates.iloc[i]['Touches in Open-play']+duplicates.iloc[i+1]['Touches in Open-play'],
                                                    duplicates.iloc[i]['Total Attempted Dribbles']+duplicates.iloc[i+1]['Total Attempted Dribbles'],
                                                    duplicates.iloc[i]['Total Successful Dribbles']+duplicates.iloc[i+1]['Total Successful Dribbles'],
                                                    ((duplicates.iloc[i]['Total Successful Dribbles']+duplicates.iloc[i+1]['Total Successful Dribbles'])/(duplicates.iloc[i]['Total Attempted Dribbles']+duplicates.iloc[i+1]['Total Attempted Dribbles']))*100,
                                                    duplicates.iloc[i]['Tackled']+duplicates.iloc[i+1]['Tackled'],
                                                    ((duplicates.iloc[i]['Tackled']+duplicates.iloc[i+1]['Tackled'])/(duplicates.iloc[i]['Total Attempted Dribbles']+duplicates.iloc[i+1]['Total Attempted Dribbles']))*100,
                                                    duplicates.iloc[i]['Carries']+duplicates.iloc[i+1]['Carries'],
                                                    duplicates.iloc[i]['Total Carrying Distance']+duplicates.iloc[i+1]['Total Carrying Distance'],
                                                    duplicates.iloc[i]['Progressive Carrying Distance']+duplicates.iloc[i+1]['Progressive Carrying Distance'],
                                                    duplicates.iloc[i]['Progressive Carries']+duplicates.iloc[i+1]['Progressive Carries'],
                                                    duplicates.iloc[i]['Carries Into Final Third']+duplicates.iloc[i+1]['Carries Into Final Third'],
                                                    duplicates.iloc[i]['Carries Into Penalty Area']+duplicates.iloc[i+1]['Carries Into Penalty Area'],
                                                    duplicates.iloc[i]['Miscontrols']+duplicates.iloc[i+1]['Miscontrols'],
                                                    duplicates.iloc[i]['Dispossessed']+duplicates.iloc[i+1]['Dispossessed'],
                                                    duplicates.iloc[i]['Passes Received']+duplicates.iloc[i+1]['Passes Received']])

        transferred_players_list.append(transferred_player_combine)

    transferred_players = pd.DataFrame(transferred_players_list)
    transferred_players.columns = dataframe.columns
    final_df = pd.concat([dataframe, transferred_players])
    final_df = final_df.reset_index(drop=True)
    return final_df   
    
    

    
    

def clean_passing(dataframe):

    dataframe.reset_index(drop=True, inplace=True)
    fixDataframe(dataframe)
    duplicates = pd.DataFrame(columns=dataframe.columns)
    duplicated_rows = dataframe[dataframe.duplicated(subset='Player', keep=False)]
    duplicates = duplicates.append(duplicated_rows)
    dataframe = dataframe.drop_duplicates(subset='Player', keep=False)
    dataframe.reset_index(drop=True, inplace=True)
    duplicates.reset_index(drop=True, inplace=True)
    duplicates = duplicates.sort_values(by='Player')

    transferred_players_list = []

    for i in range(0, len(duplicates), 2):
        if i+1 < len(duplicates):
            transferred_player_combine = pd.Series([duplicates.iloc[i]['Player'],
                                                    duplicates.iloc[i]['Passes Completed']+duplicates.iloc[i+1]['Passes Completed'],
                                                    duplicates.iloc[i]['Passes Attempted']+duplicates.iloc[i+1]['Passes Attempted'],
                                                    (duplicates.iloc[i]['Passes Completed']+duplicates.iloc[i+1]['Passes Attempted'])/(duplicates.iloc[i]['Passes Completed']+duplicates.iloc[i+1]['Passes Completed']),
                                                    duplicates.iloc[i]['TotDist']+duplicates.iloc[i+1]['TotDist'],
                                                    duplicates.iloc[i]['PrgDist']+duplicates.iloc[i+1]['PrgDist'],
                                                    duplicates.iloc[i]['Short Passes Completed']+duplicates.iloc[i+1]['Short Passes Completed'],
                                                    duplicates.iloc[i]['Short Passes Attempted']+duplicates.iloc[i+1]['Short Passes Attempted'],
                                                    ((duplicates.iloc[i]['Short Passes Completed']+duplicates.iloc[i+1]['Short Passes Completed'])/(duplicates.iloc[i]['Short Passes Attempted']+duplicates.iloc[i+1]['Short Passes Attempted']))*100 if (duplicates.iloc[i]['Short Passes Attempted']+duplicates.iloc[i+1]['Short Passes Attempted']) != 0 else 0,
                                                    duplicates.iloc[i]['Medium Passes Completed']+duplicates.iloc[i+1]['Medium Passes Completed'],
                                                    duplicates.iloc[i]['Medium Passes Attempted']+duplicates.iloc[i+1]['Medium Passes Attempted'],
                                                    ((duplicates.iloc[i]['Medium Passes Completed']+duplicates.iloc[i+1]['Medium Passes Completed'])/(duplicates.iloc[i]['Medium Passes Attempted']+duplicates.iloc[i+1]['Medium Passes Attempted']))*100 if (duplicates.iloc[i]['Medium Passes Attempted']+duplicates.iloc[i+1]['Medium Passes Attempted']) != 0 else 0,          
                                                    duplicates.iloc[i]['Long Passes Completed']+duplicates.iloc[i+1]['Long Passes Completed'],
                                                    duplicates.iloc[i]['Long Passes Attempted']+duplicates.iloc[i+1]['Long Passes Attempted'],
                                                    ((duplicates.iloc[i]['Long Passes Completed']+duplicates.iloc[i+1]['Long Passes Completed'])/(duplicates.iloc[i]['Long Passes Attempted']+duplicates.iloc[i+1]['Long Passes Attempted']))*100 if (duplicates.iloc[i]['Long Passes Attempted']+duplicates.iloc[i+1]['Long Passes Attempted']) != 0 else 0,
                                                    duplicates.iloc[i]['Expected Assists']+duplicates.iloc[i+1]['Expected Assists'],
                                                    duplicates.iloc[i]['Assists Minus Expected Goals Assistsed']+duplicates.iloc[i+1]['Assists Minus Expected Goals Assistsed'],
                                                    duplicates.iloc[i]['Key Passes']+duplicates.iloc[i+1]['Key Passes'],
                                                    duplicates.iloc[i]['Passes Into Final Third']+duplicates.iloc[i+1]['Passes Into Final Third'],
                                                    duplicates.iloc[i]['Passes Into Penalty Area']+duplicates.iloc[i+1]['Passes Into Penalty Area'],
                                                    duplicates.iloc[i]['Crosses Into Penalty Area']+duplicates.iloc[i+1]['Crosses Into Penalty Area']])                                     

        transferred_players_list.append(transferred_player_combine)

    transferred_players = pd.DataFrame(transferred_players_list)
    transferred_players.columns = dataframe.columns
    final_df = pd.concat([dataframe, transferred_players])
    final_df = final_df.reset_index(drop=True)
    return final_df
    
    
    
    
    

def clean_defending(dataframe):

    dataframe.reset_index(drop=True, inplace=True)
    fixDataframe(dataframe)
    duplicates = pd.DataFrame(columns=dataframe.columns)
    duplicated_rows = dataframe[dataframe.duplicated(subset='Player', keep=False)]
    duplicates = duplicates.append(duplicated_rows)
    dataframe = dataframe.drop_duplicates(subset='Player', keep=False)
    dataframe.reset_index(drop=True, inplace=True)
    duplicates.reset_index(drop=True, inplace=True)
    duplicates = duplicates.sort_values(by='Player')

    transferred_players_list = []

    for i in range(0, len(duplicates), 2):
        if i+1 < len(duplicates):
            if (duplicates.iloc[i]['Dribblers Challenged'] + duplicates.iloc[i+1]['Dribblers Challenged']) == 0:
                
                transferred_player_combine = pd.Series([duplicates.iloc[i]['Player'],
                                                duplicates.iloc[i]['Number Of Players Tackled']+duplicates.iloc[i+1]['Number Of Players Tackled'],
                                                duplicates.iloc[i]['Tackles Won']+duplicates.iloc[i+1]['Tackles Won'],
                                                duplicates.iloc[i]['Tackles In Defensive 3rd']+duplicates.iloc[i+1]['Tackles In Defensive 3rd'],
                                                duplicates.iloc[i]['Tackles In Middle 3rd']+duplicates.iloc[i+1]['Tackles In Middle 3rd'],
                                                duplicates.iloc[i]['Tackles In Attacking 3rd']+duplicates.iloc[i+1]['Tackles In Attacking 3rd'],
                                                0,
                                                0,
                                                0,
                                                0,
                                                duplicates.iloc[i]['Blocks']+duplicates.iloc[i+1]['Blocks'],
                                                duplicates.iloc[i]['Shots Blocked']+duplicates.iloc[i+1]['Shots Blocked'],
                                                duplicates.iloc[i]['Passes Blocked']+duplicates.iloc[i+1]['Passes Blocked'],
                                                duplicates.iloc[i]['Interceptions']+duplicates.iloc[i+1]['Interceptions'],
                                                duplicates.iloc[i]['Players Tackled Plus Interceptions']+duplicates.iloc[i+1]['Players Tackled Plus Interceptions'],
                                                duplicates.iloc[i]['Clearances']+duplicates.iloc[i+1]['Clearances'],
                                                duplicates.iloc[i]['Errors']+duplicates.iloc[i+1]['Errors']])
            
            else:
                
                transferred_player_combine = pd.Series([duplicates.iloc[i]['Player'],
                                                duplicates.iloc[i]['Number Of Players Tackled']+duplicates.iloc[i+1]['Number Of Players Tackled'],
                                                duplicates.iloc[i]['Tackles Won']+duplicates.iloc[i+1]['Tackles Won'],
                                                duplicates.iloc[i]['Tackles In Defensive 3rd']+duplicates.iloc[i+1]['Tackles In Defensive 3rd'],
                                                duplicates.iloc[i]['Tackles In Middle 3rd']+duplicates.iloc[i+1]['Tackles In Middle 3rd'],
                                                duplicates.iloc[i]['Tackles In Attacking 3rd']+duplicates.iloc[i+1]['Tackles In Attacking 3rd'],
                                                duplicates.iloc[i]['Dribblers Tackled']+duplicates.iloc[i+1]['Dribblers Tackled'],
                                                duplicates.iloc[i]['Dribblers Challenged']+duplicates.iloc[i+1]['Dribblers Challenged'],
                                                ((duplicates.iloc[i]['Dribblers Tackled']+duplicates.iloc[i+1]['Dribblers Tackled'])/(duplicates.iloc[i]['Dribblers Challenged']+duplicates.iloc[i+1]['Dribblers Challenged']))*100,
                                                duplicates.iloc[i]['Challenges Lost']+duplicates.iloc[i+1]['Challenges Lost'],
                                                duplicates.iloc[i]['Blocks']+duplicates.iloc[i+1]['Blocks'],
                                                duplicates.iloc[i]['Shots Blocked']+duplicates.iloc[i+1]['Shots Blocked'],
                                                duplicates.iloc[i]['Passes Blocked']+duplicates.iloc[i+1]['Passes Blocked'],
                                                duplicates.iloc[i]['Interceptions']+duplicates.iloc[i+1]['Interceptions'],
                                                duplicates.iloc[i]['Players Tackled Plus Interceptions']+duplicates.iloc[i+1]['Players Tackled Plus Interceptions'],
                                                duplicates.iloc[i]['Clearances']+duplicates.iloc[i+1]['Clearances'],
                                                duplicates.iloc[i]['Errors']+duplicates.iloc[i+1]['Errors']])
                                            
                                          
        transferred_players_list.append(transferred_player_combine)

    transferred_players = pd.DataFrame(transferred_players_list)
    transferred_players.columns = dataframe.columns
    final_df = pd.concat([dataframe, transferred_players])
    final_df = final_df.reset_index(drop=True)
    return final_df
