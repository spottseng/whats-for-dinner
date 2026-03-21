from rapidfuzz import process


def is_ingredient_available(ingredient_name, available_ingredients, threshold=80):
    match = process.extractOne(ingredient_name, available_ingredients)
    return match and match[1] >= threshold

def filter_missed_ingredients(missed_ingredients, available_ingredients):
    return [
        i for i in missed_ingredients
        if not is_ingredient_available(i["name"], available_ingredients)
    ]

def parse_recipes(raw_recipes, available_ingredients, max_missed, display_limit=10):
    parsed = []
    for resp in raw_recipes:
        cleaned = {
            "id": resp["id"],
            "title": resp["title"],
            "image": resp["image"],
            "used_count": resp["usedIngredientCount"],
            "missed_count": len(filter_missed_ingredients(resp["missedIngredients"], available_ingredients)),
            "used_ingredients": [i["name"] for i in resp["usedIngredients"]],
            "missed_ingredients": filter_missed_ingredients(resp["missedIngredients"], available_ingredients),
            "likes": resp["likes"],
            "url": f"https://spoonacular.com/recipes/{resp['title'].lower().replace(' ', '-')}-{resp['id']}"
        }
        parsed.append(cleaned)
    
    filtered = [r for r in parsed if r["missed_count"] <= max_missed]
    return filtered[:display_limit]
