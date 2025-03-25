document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('recipe-form');
  const clearButton = document.getElementById('clearButton');
  const recipeOutput = document.getElementById('recipeOutput');

  form.addEventListener('submit', (e) => {
      e.preventDefault();
      generateRecipe();
  });

  clearButton.addEventListener('click', () => {
      document.getElementById('ingredientInput').value = '';
      recipeOutput.innerHTML = '';
  });
});

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
  