import os
from dotenv import load_dotenv

from ingredients import load_ingredients
from api import find_by_ingredients


load_dotenv()


def main():
    ingredients = load_ingredients()

    api_key = os.environ.get("API_KEY")
    base_url = os.environ.get("BASE_URL")
    num_recipes = os.environ.get("NUM_RECIPES")    

    
    response = find_by_ingredients(base_url, api_key, num_recipes, ingredients)
    print(response.json())

if __name__ == "__main__":
    main()