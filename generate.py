# In generate.py
import config
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

# The path to your saved model folder
MODEL_DIR = config.OUTPUT_DIR 

# --- Load the Tokenizer and Model ---
print(f"Loading model from {MODEL_DIR}...")
try:
    tokenizer = T5Tokenizer.from_pretrained(MODEL_DIR)
    model = T5ForConditionalGeneration.from_pretrained(MODEL_DIR)
    
    # Check if you have a GPU (this runs the local check)
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Running on device: {DEVICE}")
    model.to(DEVICE) 
    model.eval() # Set model to evaluation mode
    print("✅ Model loaded successfully.")

except Exception as e:
    print(f"Error loading model: {e}")
    print(f"Make sure the directory '{MODEL_DIR}' exists.")
    exit()


def generate_recipe(ingredients_list):
    """
    Takes a list of ingredients and generates a recipe.
    """
    if not ingredients_list:
        print("Please provide a list of ingredients.")
        return

    # 1. Format the input just like your training data
    ingredients_str = ", ".join(ingredients_list)
    input_text = f"generate recipe: {ingredients_str}"
    
    # 2. Tokenize the input text
    inputs = tokenizer(
        input_text, 
        return_tensors="pt", 
        max_length=config.MAX_INPUT_LENGTH,
        padding=True, 
        truncation=True
    ).to(DEVICE) # Send the input to your CPU or GPU

    # 3. Generate the output
    print("\nGenerating recipe...")
    with torch.no_grad():
        outputs = model.generate(
            inputs['input_ids'],
            max_length=config.MAX_TARGET_LENGTH, # Max words in output
            num_beams=4,          # Use "beam search" for better results
            early_stopping=True   # Stop when the model finishes
        )
    
    # 4. Decode the generated tokens back into text
    generated_text = tokenizer.decode(
        outputs[0], 
        skip_special_tokens=True
    )
    
    return generated_text

# --- Main program to run ---
if __name__ == "__main__":
    
    # Try your own ingredients here!
    my_ingredients = ["flour", "sugar", "eggs", "butter", "chocolate"]
    
    # Generate the recipe
    recipe = generate_recipe(my_ingredients)
    
    print("---" * 10)
    print(f"INGREDIENTS: {', '.join(my_ingredients)}")
    print("\nGENERATED RECIPE:")
    print(recipe)
    print("---" * 10)