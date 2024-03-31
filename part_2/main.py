import json

import pandas as pd

PROJECT_ABSOLUTE_PATH = '/Users/camilo.leon/Desktop/python/etl-usda-ingredients'
OUTPUT_FOLDER_PATH = f'{PROJECT_ABSOLUTE_PATH}/part_2/data/output'
INPUT_FOLDER_PATH = f'{PROJECT_ABSOLUTE_PATH}/part_2/data/input'

CODE_NUTRIENT_CHOLESTEROL = '601'
CODE_NUTRIENT_TOTAL_SATURATED = '606'
CODE_NUTRIENT_SODIUM = '307'
CODE_NUTRIENT_PROTEIN = '203'
CODE_NUTRIENT_MAGNESIUM = '304'
CODE_NUTRIENT_IRON = '303'
CODE_NUTRIENT_FOLIC_ACID = '431'


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


def sort_ingredients_by_nutrient(ingredients, code_nutrient, limit=200):
    return sorted(ingredients,
                  key=lambda ingredient: retrieve_nutrient_value(ingredient=ingredient, code_nutrient=code_nutrient),
                  reverse=True)[:limit]


def find_matches(list1, list2):
    _matches = []
    for elem1 in list1:
        for elem2 in list2:
            if elem1 == elem2:
                _matches.append(elem1)
    return _matches


def process_positive_list(ingredients):
    protein_list = sort_ingredients_by_nutrient(ingredients=ingredients, code_nutrient=CODE_NUTRIENT_PROTEIN, limit=200)
    magnesium_list = sort_ingredients_by_nutrient(ingredients=ingredients, code_nutrient=CODE_NUTRIENT_MAGNESIUM, limit=80)
    iron_list = sort_ingredients_by_nutrient(ingredients=ingredients, code_nutrient=CODE_NUTRIENT_IRON, limit=80)
    folic_acid_list = sort_ingredients_by_nutrient(ingredients=ingredients, code_nutrient=CODE_NUTRIENT_FOLIC_ACID, limit=80)

    total_list = protein_list + magnesium_list + iron_list + folic_acid_list
    total_dict = {}
    for item in total_list:
        code = item.get('code')
        name = item.get('name')

        registered_item = total_dict.get(code)
        if registered_item:
            item_to_upsert = {
                **registered_item,
                "positive_count": registered_item.get("positive_count") + 1
            }

        else:
            item_to_upsert = {
                "code": code,
                "name": name,
                "protein": retrieve_nutrient_value(ingredient=item, code_nutrient=CODE_NUTRIENT_PROTEIN),
                "magnesium": retrieve_nutrient_value(ingredient=item, code_nutrient=CODE_NUTRIENT_MAGNESIUM),
                "iron": retrieve_nutrient_value(ingredient=item, code_nutrient=CODE_NUTRIENT_IRON),
                "folic_acid": retrieve_nutrient_value(ingredient=item, code_nutrient=CODE_NUTRIENT_FOLIC_ACID),
                "positive_count": 1
            }

        total_dict[code] = item_to_upsert

    return pd.DataFrame.from_dict(total_dict, orient="index")


def process_nutrient_list(ingredients, code_nutrient, limit=None):
    nutrient_list = sort_ingredients_by_nutrient(ingredients=ingredients, code_nutrient=code_nutrient, limit=limit)
    items = []
    for nutrient_item in nutrient_list:
        item = {
            'code': nutrient_item.get('code'),
            'name': nutrient_item.get('name'),
            'value': retrieve_nutrient_value(ingredient=nutrient_item, code_nutrient=code_nutrient)
        }
        items.append(item)
    return pd.DataFrame(items)


def process_matches(list1, list2, code_nutrients):
    matches = find_matches(list1=list1, list2=list2)
    items = []
    for match in matches:
        item = {
            'code': match.get('code'),
            'name': match.get('name'),
            'value1': retrieve_nutrient_value(ingredient=match, code_nutrient=code_nutrients[0]),
            'value2': retrieve_nutrient_value(ingredient=match, code_nutrient=code_nutrients[1])}
        items.append(item)
    return pd.DataFrame(items)


if __name__ == '__main__':
    input_filename = "data.json"
    ingredients = read_json_to_dict(path=f'{INPUT_FOLDER_PATH}/{input_filename}')

    cholesterol_list = sort_ingredients_by_nutrient(ingredients=ingredients, code_nutrient=CODE_NUTRIENT_CHOLESTEROL)
    total_saturated_list = sort_ingredients_by_nutrient(ingredients=ingredients,
                                                        code_nutrient=CODE_NUTRIENT_TOTAL_SATURATED)
    df_matches = process_matches(list1=cholesterol_list,list2=total_saturated_list, code_nutrients=[CODE_NUTRIENT_CHOLESTEROL, CODE_NUTRIENT_TOTAL_SATURATED])

    df_sodium = process_nutrient_list(ingredients, CODE_NUTRIENT_SODIUM)
    df_positive = process_positive_list(ingredients)

    output_filename = "output.xlsx"
    path_file = f'{OUTPUT_FOLDER_PATH}/{output_filename}'
    with pd.ExcelWriter(path_file) as writer:
        df_matches.to_excel(writer, sheet_name="Matches C-S", index=False)
        df_sodium.to_excel(writer, sheet_name="Sodium", index=False)
        df_positive.to_excel(writer, sheet_name="Positive", index=False)
