import json
from flask import Flask, jsonify, send_from_directory

app = Flask(__name__)

# Load the recipes from the JSON file at startup
with open('recipes_clean_1000.json', 'r', encoding='utf-8') as f:
    recipes_data = json.load(f)

# Define an API endpoint to serve the recipes
@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    return jsonify({'recipes': recipes_data})

# Serve the static HTML file
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index_new.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)