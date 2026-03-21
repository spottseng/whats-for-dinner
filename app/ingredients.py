import yaml
import os


def load_ingredients():
    full_path = os.path.join(os.path.dirname(__file__), "../fridge.yaml")
    
    with open(full_path, "r") as f:
        data = yaml.safe_load(f)

    ingredients = []
    for section in data.values():
        if isinstance(section, list):
            ingredients.extend(section)
        elif isinstance(section, dict):
            for subsection in section.values():
                if isinstance(subsection, list) and subsection:
                    ingredients.extend(subsection)
            
    return ingredients
     
