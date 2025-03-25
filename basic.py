import json
import anthropic
import os
from dotenv import load_dotenv
from recipe_ml import recommender

load_dotenv()

api_key = os.getenv('ANTHROPIC_API_KEY')
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

client = anthropic.Anthropic()

def get_recipe(ingredients, preferences=None):
    try:
        # Get similar recipes from our ML system
        similar_recipes = recommender.find_similar_recipes(ingredients)
        
        # Get suggested ingredients
        suggested_ingredients = recommender.suggest_ingredients(ingredients)
        
        # Convert preferences dict to string
        pref_str = ""
        if preferences:
            pref_str = "Please ensure the recipe follows these dietary requirements:\n"
            for pref, value in preferences.items():
                if value and pref != 'ingredients':
                    pref_str += f"- {pref}\n"
        
        # Add ML-based context to the prompt
        ml_context = ""
        if similar_recipes:
            ml_context = "\nSimilar recipes in our database:\n"
            for recipe in similar_recipes:
                ml_context += f"- {recipe['name']} (uses: {', '.join(recipe['ingredients'])})\n"
        
        if suggested_ingredients:
            ml_context += f"\nSuggested additional ingredients: {', '.join(suggested_ingredients)}\n"
        
        prompt = f"""Create a recipe using these ingredients: {', '.join(ingredients)}

{pref_str}

{ml_context}

Please format the response as follows:
1. Recipe name
2. Ingredients section (with measurements)
3. Instructions section (step by step)
4. Nutritional information
5. Cooking time and difficulty level

If any additional ingredients are needed beyond what was provided, please list them separately."""

        # Use claude-3-haiku which is more cost-effective
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Extract recipe name and ingredients from the response
        recipe_text = response.content[0].text
        recipe_name = recipe_text.split('\n')[0]
        
        # Parse ingredients from the response
        ingredients_section = ""
        for line in recipe_text.split('\n'):
            if 'ingredients' in line.lower() and ':' in line:
                ingredients_section = line
                break
        
        # Add the recipe to our ML system
        if recipe_name and ingredients_section:
            parsed_ingredients = [ing.strip().strip('- ') for ing in ingredients_section.split('\n')[1:] if ing.strip()]
            recommender.add_recipe(recipe_name, parsed_ingredients, recipe_text)
        
        return recipe_text
    except anthropic.APIError as e:
        if "insufficient_quota" in str(e) or "invalid_api_key" in str(e):
            raise Exception("API quota exceeded or invalid API key. Please check your Anthropic account settings and billing information.")
        raise e
    except Exception as e:
        raise Exception(f"Error generating recipe: {str(e)}")

def format_recipe(recipe_text):
    sections = {
        'name': '',
        'ingredients': [],
        'instructions': [],
        'nutrition': '',
        'info': ''
    }
    
    current_section = 'name'
    lines = recipe_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if 'ingredients' in line.lower() and ':' in line:
            current_section = 'ingredients'
            continue
        elif 'instructions' in line.lower() and ':' in line:
            current_section = 'instructions'
            continue
        elif 'nutritional' in line.lower() and ':' in line:
            current_section = 'nutrition'
            continue
        elif 'cooking time' in line.lower() or 'difficulty' in line.lower():
            current_section = 'info'
            sections[current_section] += line + '\n'
            continue
            
        if current_section == 'name' and not sections['name']:
            sections['name'] = line
        elif current_section == 'ingredients':
            if line.strip() and not line.startswith('-'):
                sections['ingredients'].append(f"- {line}")
            else:
                sections['ingredients'].append(line)
        elif current_section == 'instructions':
            if line.strip():
                clean_line = line.lstrip('0123456789.) ')
                sections['instructions'].append(clean_line)
        elif current_section == 'nutrition':
            sections['nutrition'] += line + '\n'
        elif current_section == 'info':
            sections['info'] += line + '\n'

    # Format the final output
    formatted_recipe = f"{sections['name']}\n\n"
    formatted_recipe += "Ingredients:\n" + '\n'.join(sections['ingredients']) + '\n\n'
    formatted_recipe += "Instructions:\n" + '\n'.join(f"{i+1}. {inst}" for i, inst in enumerate(sections['instructions'])) + '\n\n'
    formatted_recipe += "Nutritional Information:\n" + sections['nutrition'] + '\n'
    formatted_recipe += "Additional Information:\n" + sections['info']

    return formatted_recipe

def main():
    print("Welcome to your personal AI Chef!")
    ingredients = input("Enter the ingredients you have (comma separated): ").split(',')

    # Clean up ingredients list
    ingredients = [ingredient.strip() for ingredient in ingredients]

    recipe_response = get_recipe(ingredients)

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
        return

    formatted_recipe = format_recipe(recipe_text)
    print(formatted_recipe)

if __name__ == "__main__":
    main()

