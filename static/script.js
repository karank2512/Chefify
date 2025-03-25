document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('recipe-form');
    const loadingSpinner = document.getElementById('loading');
    const recipeOutput = document.getElementById('recipe-output');
    const recipeText = document.getElementById('recipe-text');
    const clearButton = document.getElementById('clear-button');
    const veganCheckbox = document.getElementById('vegan');
    const vegetarianCheckbox = document.getElementById('vegetarian');

    // When vegan is selected, automatically select vegetarian
    veganCheckbox.addEventListener('change', function() {
        if (this.checked) {
            vegetarianCheckbox.checked = true;
        }
    });

    // Prevent unchecking vegetarian if vegan is checked
    vegetarianCheckbox.addEventListener('change', function() {
        if (!this.checked && veganCheckbox.checked) {
            this.checked = true;
        }
    });

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const ingredients = document.getElementById('ingredients').value.trim();
        if (!ingredients) {
            alert('Please enter some ingredients!');
            return;
        }

        // Show loading spinner
        loadingSpinner.style.display = 'flex';
        recipeOutput.style.display = 'none';
        
        // Collect all preferences
        const preferences = {
            ingredients: ingredients,
            vegetarian: document.getElementById('vegetarian').checked,
            vegan: document.getElementById('vegan').checked,
            gluten_free: document.getElementById('gluten_free').checked,
            dairy_free: document.getElementById('dairy_free').checked,
            high_protein: document.getElementById('high_protein').checked,
            low_carb: document.getElementById('low_carb').checked,
            keto: document.getElementById('keto').checked,
            paleo: document.getElementById('paleo').checked
        };

        try {
            const response = await fetch('/generate_recipe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(preferences)
            });

            const data = await response.json();
            
            if (data.success) {
                recipeText.textContent = data.recipe;
                recipeOutput.style.display = 'block';
            } else {
                alert('Error: ' + (data.error || 'Failed to generate recipe'));
            }
        } catch (error) {
            alert('Error: Failed to connect to the server');
            console.error('Error:', error);
        } finally {
            loadingSpinner.style.display = 'none';
        }
    });

    clearButton.addEventListener('click', function() {
        // Clear form inputs
        form.reset();
        
        // Hide recipe output
        recipeOutput.style.display = 'none';
    });
}); 