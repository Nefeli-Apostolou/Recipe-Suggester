# In data_cleaning_utils.py
import re
import json

def sanitize_text_for_json(text):
    """
    Aggressively cleans text to ensure it's safe to
    be a value in a JSON string.
    """
    if not isinstance(text, str):
        text = str(text)
    
    # Remove all characters that could break a JSON string.
    text = text.replace('"', '')  # Remove double quotes
    text = text.replace('\\', '') # Remove backslashes
    text = text.replace('\n', ' ') # Remove newlines
    text = text.replace('\r', ' ') # Remove carriage returns
    text = text.replace('\t', ' ') # Remove tabs
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def simplify_category(cat):
    if not isinstance(cat, str) or cat.strip() == "":
        return "savory"
    cat = cat.lower()
    dessert_keywords = ["dessert", "cake", "cookie", "pie", "pudding", "brownie", "chocolate", "ice cream", "sweet"]
    beverage_keywords = ["drink", "beverage", "juice", "smoothie", "coffee", "tea", "cocktail", "punch"]
    if any(word in cat for word in dessert_keywords):
        return "dessert"
    elif any(word in cat for word in beverage_keywords):
        return "beverages"
    else:
        return "savory"

def parse_ingredients(ing_str):
    if not isinstance(ing_str, str):
        return []
    
    cleaned_ingredients = []
    
    try:
        ingredients = json.loads(ing_str)
        if isinstance(ingredients, list):
            cleaned_ingredients = [sanitize_text_for_json(str(i).lower()) for i in ingredients if isinstance(i, (str, int, float))]
    except json.JSONDecodeError:
        pass  # Will be caught by the next blocks

    if not cleaned_ingredients and ing_str.strip().startswith("c("):
        matches = re.findall(r'\"([^\"]+)\"', ing_str)
        cleaned_ingredients = [sanitize_text_for_json(m.lower()) for m in matches]

    if not cleaned_ingredients:
        matches = re.findall(r"['\\\"]([^'\\\"]+)['\\\"]", ing_str)
        if matches:
            cleaned_ingredients = [sanitize_text_for_json(m.lower()) for m in matches]
            
    cleaned_ingredients = [i for i in cleaned_ingredients if i]
    unique_ingredients = list(set(cleaned_ingredients))
    return unique_ingredients

def infer_diet(ingredients):
    non_veg = ["chicken", "beef", "pork", "fish", "shrimp", "bacon", "turkey"]
    dairy_eggs = ["milk", "cheese", "butter", "cream", "egg", "yogurt"]
    ingredients_str = " ".join(ingredients)
    if any(item in ingredients_str for item in non_veg):
        return "non-vegetarian"
    if any(item in ingredients_str for item in dairy_eggs):
        return "vegetarian"
    return "vegan"

def infer_gluten(ingredients):
    gluten_sources = ["wheat", "flour", "barley", "rye", "pasta", "bread"]
    ingredients_str = " ".join(ingredients)
    if any(item in ingredients_str for item in gluten_sources):
        return "contains gluten"
    return "gluten-free"

def parse_instructions(inst_str):
    if not isinstance(inst_str, str) or inst_str.strip() == "":
        return ""
    text = ""
    try:
        steps = json.loads(inst_str)
        if isinstance(steps, list):
            text = ". ".join(str(step) for step in steps)
        else:
            text = str(steps)
    except json.JSONDecodeError:
        matches = re.findall(r'\"(.*?)\"', inst_str)
        if matches:
            text = ". ".join(matches)
        else:
            text = inst_str
            
    text = sanitize_text_for_json(text)
    return text