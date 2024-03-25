def build_ingredient_from_df_ingredient(df_ingredient):
    ingredient_code = str(df_ingredient.loc[0]['Ingredient code'])
    ingredient_name = df_ingredient.loc[0]['Ingredient description']

    nutrients = []
    for _, row in df_ingredient.iterrows():
        nutrient = {
            "code_nutrient": str(row['Nutrient code']),
            "description": row['Nutrient description'],
            "value": float(row['Nutrient value']),
            "source": row['Nutrient value source']
        }
        nutrients.append(nutrient)

    ingredient = {
        "code": ingredient_code,
        "name": ingredient_name,
        "nutrients": nutrients
    }
    return ingredient


def retrieve_df_ingredient_by_code(df, code):
    df_ingredient = df[df['Ingredient code'] == code]
    df_ingredient = df_ingredient.reset_index(drop=True)
    return df_ingredient


def retrieve_ingredient_codes(df):
    return df['Ingredient code'].unique()


def retrieve_ingredients_from_df(df):
    ingredient_codes = retrieve_ingredient_codes(df)
    ingredients = []
    for code in ingredient_codes:
        df_ingredient = retrieve_df_ingredient_by_code(df=df, code=code)
        ingredient = build_ingredient_from_df_ingredient(df_ingredient=df_ingredient)
        ingredients.append(ingredient)
    return ingredients


