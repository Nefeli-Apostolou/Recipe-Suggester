import config
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- 1. Initialize Flask App ---
app = Flask(__name__)
CORS(app)  # This allows your HTML file to make requests

# --- 2. Load Your AI Model (Only ONCE) ---
print("Loading model and tokenizer... This may take a moment.")
MODEL_DIR = config.OUTPUT_DIR
tokenizer = T5Tokenizer.from_pretrained(MODEL_DIR)
model = T5ForConditionalGeneration.from_pretrained(MODEL_DIR)

# Check for GPU (if you have one locally) or use CPU
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model.to(DEVICE)
model.eval()  # Set model to "evaluation" mode
print(f"✅ Model loaded successfully on {DEVICE}.")

# --- 3. Create the Generation Function ---
def generate_recipe_from_model(ingredients_list):
    """Takes a list of ingredients and returns the model's text output."""

    # Format the input for the T5 model
    ingredients_str = ", ".join(ingredients_list)
    input_text = f"generate recipe: {ingredients_str}"

    # Tokenize the input
    inputs = tokenizer(
        input_text, 
        return_tensors="pt", 
        max_length=config.MAX_INPUT_LENGTH,
        padding=True, 
        truncation=True
    ).to(DEVICE)

    # Generate the recipe text
    with torch.no_grad():
        outputs = model.generate(
            inputs['input_ids'],
            max_length=config.MAX_TARGET_LENGTH,
            num_beams=4,
            early_stopping=True
        )

    # Decode the text
    generated_text = tokenizer.decode(
        outputs[0], 
        skip_special_tokens=True
    )
    return generated_text

# --- 4. Create the API Endpoint ---
# This is the URL your app will send requests to
@app.route('/api/generate', methods=['POST'])
def handle_generation():
    # Get the ingredients from the app's request
    data = request.get_json()
    ingredients = data.get('ingredients')

    if not ingredients:
        return jsonify({'error': 'No ingredients provided'}), 400

    print(f"Generating recipe for: {ingredients}")

    # Call your AI model
    try:
        recipe_text = generate_recipe_from_model(ingredients)
        # Send the generated text back to the app
        return jsonify({'recipe': recipe_text})
    except Exception as e:
        print(f"Error during generation: {e}")
        return jsonify({'error': 'Failed to generate recipe'}), 500

# --- 5. Run the Server ---
if __name__ == '__main__':
    # This starts the web server on http://localhost:5000
    app.run(host='0.0.0.0', port=5000)