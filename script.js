function generateRecipe() {
    const ingredientInput = document.getElementById('ingredientInput');
    const recipeOutput = document.getElementById('recipeOutput');
  
    const ingredients = ingredientInput.value;
  
    // Send a request to the backend with the ingredients
    fetch('/generate_recipe', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ ingredients: ingredients })
    })
    .then(response => response.json())
    .then(data => {
      recipeOutput.textContent = data.recipe;
    })
    .catch(error => {
      console.error('Error:', error);
      recipeOutput.textContent = 'An error occurred.';
    });
  }
  