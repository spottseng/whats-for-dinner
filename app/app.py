import os
from dotenv import load_dotenv

from ingredients import load_ingredients
from api import find_by_ingredients, get_recipe_url
from recommender import parse_recipes

import streamlit as st


load_dotenv()

api_key = os.environ.get("API_KEY")
base_url = os.environ.get("BASE_URL")
num_recipes = os.environ.get("NUM_RECIPES")
missing_limit = int(os.environ.get("MISSING_LIMIT"))

ingredients = load_ingredients()

if "recipe_urls" not in st.session_state:
    st.session_state.recipe_urls = {}

@st.cache_data
def fetch_recipes(ingredients, base_url, api_key, num_recipes, missing_limit):
    response = find_by_ingredients(base_url, api_key, num_recipes, ingredients)
    recipes = parse_recipes(response, ingredients, missing_limit)
    for recipe in recipes:
        recipe["url"] = get_recipe_url(base_url, api_key, recipe["id"])
    recipes = recipes.sort(key=lambda r: r["missed_count"])
    return recipes

st.title("Gordon Ramsage")

with st.spinner("Checking your fridge..."):
    recipes = fetch_recipes(tuple(ingredients), base_url, api_key, num_recipes, missing_limit)

for recipe in recipes:
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(recipe["image"])
    with col2:
        st.subheader(recipe["title"])
        st.write(f"Uses {recipe['used_count']} of your ingredients")
        st.write(f"Missing {recipe['missed_count']} ingredients")
        if recipe["missed_ingredients"]:
            st.write("You'll need: " + ", ".join([i["name"] for i in recipe["missed_ingredients"]]))

        st.link_button("View Recipe", recipe["url"])
    st.divider()
