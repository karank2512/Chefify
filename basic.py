import json
import anthropic

client = anthropic.Anthropic("api_key")

def get_recipe(ingredients):
    prompt = f"Suggest a recipe that can be made with the following ingredients: {', '.join(ingredients)}"
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        messages=[{"role":"user", "content":prompt}]
        
    )
    return response.content

def format_recipe(recipe_text):
    lines = recipe_text.split('\n')
    recipe_name = lines[0].strip()

    ingredients_section = False
    instructions_section = False

    ingredients = []
    instructions = []

    for line in lines[1:]:
        if line.lower().startswith('ingredients:'):
            ingredients_section = True
            instructions_section = False
            continue
        elif line.lower().startswith('instructions:'):
            ingredients_section = False
            instructions_section = True
            continue

        if ingredients_section:
            if line.strip() and not line.startswith('-'):
                ingredients.append(f"- {line.strip()}")
            elif line.startswith('-'):
                ingredients.append(line.strip())
        elif instructions_section:
            if line.strip() and not line.lstrip().isdigit():
                clean_line = line.lstrip('0123456789. ')
                instructions.append(clean_line)

    formatted_ingredients = '\n'.join(ingredients)
    formatted_instructions = '\n'.join([f"{i+1}. {instruction}" for i, instruction in enumerate(instructions)])

    formatted_recipe = f"{recipe_name}\n\nIngredients:\n{formatted_ingredients}\n\nRecipe:\n{formatted_instructions}"
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

