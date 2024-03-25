import json

import pandas as pd

from retrieve_ingredients import retrieve_ingredients_from_df

PROJECT_ABSOLUTE_PATH = '/Users/camilo.leon/Desktop/python/etl-usda-ingredients'
OUTPUT_FOLDER_PATH = f'{PROJECT_ABSOLUTE_PATH}/part_1/data/output'
INPUT_FOLDER_PATH = f'{PROJECT_ABSOLUTE_PATH}/part_1/data/input'


def get_df_from_excel(path):
    return pd.read_excel(path, header=1)


def save_to_json(path):
    with open(path, "w") as file:
        json.dump(ingredients, file)


if __name__ == '__main__':
    input_filename = "2019-2020 FNDDS At A Glance - Ingredient Nutrient Values.xlsx"
    output_filename = "data.json"

    df = get_df_from_excel(path=f'{INPUT_FOLDER_PATH}/{input_filename}')

    ingredients = retrieve_ingredients_from_df(df=df)

    save_to_json(path=f'{OUTPUT_FOLDER_PATH}/{output_filename}')
