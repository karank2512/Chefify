import json
import traceback
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import basic

app = Flask(__name__)
CORS(app)

# Configure static files to use relative paths
app.static_folder = 'static'
app.static_url_path = '/static'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_recipe', methods=['POST'])
def generate_recipe_endpoint():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        ingredients = data.get('ingredients', '').split(',')
        ingredients = [ingredient.strip() for ingredient in ingredients if ingredient.strip()]
        
        if not ingredients:
            return jsonify({"error": "No ingredients provided"}), 400
            
        # Get dietary preferences
        preferences = {
            'vegetarian': data.get('vegetarian', False),
            'vegan': data.get('vegan', False),
            'gluten_free': data.get('gluten_free', False),
            'dairy_free': data.get('dairy_free', False),
            'high_protein': data.get('high_protein', False),
            'low_carb': data.get('low_carb', False),
            'keto': data.get('keto', False),
            'paleo': data.get('paleo', False)
        }

        recipe_text = basic.get_recipe(ingredients, preferences)
        formatted_recipe = basic.format_recipe(recipe_text)

        return jsonify({
            "success": True,
            "recipe": formatted_recipe
        })
        
    except Exception as e:
        app.logger.error(f"Error generating recipe: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route('/clear_recipe', methods=['POST'])
def clear_recipe():
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)
