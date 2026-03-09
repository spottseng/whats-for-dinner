import requests

def find_by_ingredients(base_url, api_key, num_recipes, ingredients):
    endpoint = f"{base_url}/recipes/findByIngredients"
    params = {
        "apiKey": api_key,
        "ingredients": ",".join(ingredients),
        "number": num_recipes,
        "ranking": 1,  # 1 = maximize used ingredients, 2 = minimize missing
        "ignorePantry": False
    }
    
    response = requests.get(endpoint, params=params)
    response.raise_for_status() 

    return response

