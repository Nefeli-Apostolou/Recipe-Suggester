# In build_dataset.py
import pandas as pd
import json
import re
from data_cleaning_utils import (
    parse_ingredients,
    parse_instructions,
    simplify_category,
    infer_diet,
    infer_gluten,
    sanitize_text_for_json  # Import the master sanitizer
)

# --- Configuration ---
input_file = 'recipes.csv'
output_file_json = 'recipes_clean.json' 
output_file_training = 'recipes_training.jsonl' # The T5 training file

# --- Main Script Workflow ---
print(f"Loading data from {input_file}...")
columns_to_load = [
    "Name", "RecipeCategory", "Calories", "FatContent",
    "CarbohydrateContent", "ProteinContent", "RecipeInstructions",
    "RecipeIngredientParts"
]

try:
    df = pd.read_csv(input_file, usecols=columns_to_load)
    print("Cleaning and filtering the full dataset...")

    # 1. Drop rows with missing critical fields
    df.dropna(subset=columns_to_load, inplace=True)

    # 2. Parse and SANITIZE all text fields
    df["ingredients_list"] = df["RecipeIngredientParts"].apply(parse_ingredients)
    df["instructions_clean"] = df["RecipeInstructions"].apply(parse_instructions)
    df["name_clean"] = df["Name"].apply(sanitize_text_for_json) # Sanitize the name!

    # 3. Filter for good data
    df = df[df["ingredients_list"].str.len() > 1]
    df = df[df["instructions_clean"].str.len() > 20] 
    
    # 4. Apply all other cleaning functions
    df["category_clean"] = df["RecipeCategory"].apply(simplify_category)
    df["diet_inferred"] = df["ingredients_list"].apply(infer_diet)
    df["gluten_inferred"] = df["ingredients_list"].apply(infer_gluten)

    # 5. Build and save the final files
    print(f"Building final output files...")
    recipes_for_json = []
    
    with open(output_file_training, "w", encoding="utf-8") as f_train:
        for _, row in df.iterrows():
            
            recipe_obj = {
                "name": row["name_clean"],
                "category": row["category_clean"],
                "calories": row["Calories"],
                "fat": row["FatContent"],
                "carbs": row["CarbohydrateContent"],
                "protein": row["ProteinContent"],
                "instructions": row["instructions_clean"],
                "ingredients": row["ingredients_list"],
                "diet": row["diet_inferred"],
                "gluten": row["gluten_inferred"]
            }
            recipes_for_json.append(recipe_obj)
            
            # This is the T5 record. All fields are now clean.
            ingredients_str = ", ".join(sorted(row["ingredients_list"]))
            input_text = f"generate recipe: {ingredients_str}"
            target_text = f"name: {row['name_clean']} instructions: {row['instructions_clean']}"
            
            training_line = {"input": input_text, "target": target_text}
            
            # Final safety check before writing
            try:
                f_train.write(json.dumps(training_line) + "\n")
            except Exception as e:
                print(f"ERROR: Could not write row: {row['Name']}")
                print(f"   Input: {input_text}")
                print(f"   Target: {target_text}")
                print(f"   Error: {e}")

    with open(output_file_json, "w", encoding="utf-8") as f:
        json.dump(recipes_for_json, f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully saved {len(recipes_for_json)} recipes to {output_file_json}")
    print(f"✅ Successfully saved training data to {output_file_training}")
    
except FileNotFoundError:
    print(f"Error: The file '{input_file}' was not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")