import os

from pandas import DataFrame


def saveDataframe(df: DataFrame, fileName):
    output_folder = '../data'

    current_directory = os.getcwd()
    output_path = os.path.join(current_directory, output_folder, fileName)
    df.to_excel(output_path, index=False)
