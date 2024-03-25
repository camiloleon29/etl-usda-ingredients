import json

import pandas as pd

PROJECT_ABSOLUTE_PATH = '/Users/camilo.leon/Desktop/python/etl-usda-ingredients'
OUTPUT_FOLDER_PATH = f'{PROJECT_ABSOLUTE_PATH}/part_2/data/output'
INPUT_FOLDER_PATH = f'{PROJECT_ABSOLUTE_PATH}/part_2/data/input'

CODE_NUTRIENT_CHOLESTEROL = '601'
CODE_NUTRIENT_TOTAL_SATURATED = '606'
CODE_NUTRIENT_SODIUM = '307'


def read_json_to_dict(path):
    with open(path, "r") as file:
        data = json.load(file)
    return data


def retrieve_nutrient_value(ingredient, code_nutrient):
    nutrients = ingredient.get('nutrients')
    for nutrient in nutrients:
        if nutrient.get('code_nutrient') == code_nutrient:
            return nutrient.get('value')
    return 0


def sort_ingredients_by_nutrient(ingredients, code_nutrient, limit=200 ):
    return sorted(ingredients, key=lambda ingredient: retrieve_nutrient_value(ingredient=ingredient, code_nutrient=code_nutrient), reverse=True)[:limit]


def find_matches(list1, list2):
    _matches = []
    for elem1 in list1:
        for elem2 in list2:
            if elem1 == elem2:
                _matches.append(elem1)
    return _matches


if __name__ == '__main__':
    input_filename = "data.json"
    output_filename = "output.xlsx"
    ingredients = read_json_to_dict(path=f'{INPUT_FOLDER_PATH}/{input_filename}')

    cholesterol_list = sort_ingredients_by_nutrient(ingredients=ingredients, code_nutrient=CODE_NUTRIENT_CHOLESTEROL)
    total_saturated_list = sort_ingredients_by_nutrient(ingredients=ingredients, code_nutrient=CODE_NUTRIENT_TOTAL_SATURATED)

    matches = find_matches(list1=cholesterol_list, list2=total_saturated_list)
    items = []
    for match in matches:
        item = {
            'code':  match.get('code'),
            'name': match.get('name'),
            'cholesterol':retrieve_nutrient_value(ingredient=match,code_nutrient=CODE_NUTRIENT_CHOLESTEROL),
            'total_saturated':retrieve_nutrient_value(ingredient=match,code_nutrient=CODE_NUTRIENT_TOTAL_SATURATED)}
        items.append(item)
    df = pd.DataFrame(items)
    df.to_excel(f'{OUTPUT_FOLDER_PATH}/{output_filename}')
