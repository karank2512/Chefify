import json
from flask import Flask, render_template, request, jsonify
import basic

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_recipe', methods=['POST'])
def generate_recipe_endpoint():
    
    ingredients = request.form['ingredients']

    ingredients_list = [ingredient.strip() for ingredient in ingredients]

    recipe_response = basic.get_recipe(ingredients_list)

    if isinstance(recipe_response, list):
        for element in recipe_response:
            if hasattr(element, 'content'):
                recipe_text = element.content[0].text
                break
            elif hasattr(element, 'text'):
                recipe_text = element.text
                break
            else:
                try:
                    element_json = json.loads(str(element))
                except json.JSONDecodeError:
                    print("Error parsing JSON")
    elif hasattr(recipe_response, 'content'):
        recipe_text = recipe_response.content[0].text
    else:
        print("Error: Unexpected response format.")
        return jsonify({"error": "Unexpected response format."}), 500

    formatted_recipe = basic.format_recipe(recipe_text)

    return render_template('index.html', recipe=formatted_recipe)

@app.route('/clear_recipe', methods=['POST'])
def clear_recipe():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
