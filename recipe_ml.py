import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os
from collections import Counter

class RecipeRecommender:
    def __init__(self):
        self.recipes_file = 'recipes_data.json'
        self.vectorizer = TfidfVectorizer()
        self.recipes_data = self._load_recipes()
        self.ingredient_frequencies = self._calculate_ingredient_frequencies()
        
    def _load_recipes(self):
        if os.path.exists(self.recipes_file):
            with open(self.recipes_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_recipes(self):
        with open(self.recipes_file, 'w') as f:
            json.dump(self.recipes_data, f)
    
    def _calculate_ingredient_frequencies(self):
        all_ingredients = []
        for recipe in self.recipes_data:
            all_ingredients.extend(recipe['ingredients'])
        return Counter(all_ingredients)
    
    def add_recipe(self, recipe_name, ingredients, instructions):
        """Add a new recipe to the database"""
        recipe = {
            'name': recipe_name,
            'ingredients': ingredients,
            'instructions': instructions
        }
        self.recipes_data.append(recipe)
        self._save_recipes()
        self.ingredient_frequencies = self._calculate_ingredient_frequencies()
    
    def get_popular_ingredients(self, top_n=10):
        """Get the most commonly used ingredients"""
        return self.ingredient_frequencies.most_common(top_n)
    
    def suggest_ingredients(self, current_ingredients, top_n=5):
        """Suggest additional ingredients based on current ingredients"""
        if not current_ingredients:
            return [ingredient for ingredient, _ in self.get_popular_ingredients(top_n)]
        
        # Find recipes that use any of the current ingredients
        related_ingredients = set()
        for recipe in self.recipes_data:
            if any(ing in recipe['ingredients'] for ing in current_ingredients):
                related_ingredients.update(recipe['ingredients'])
        
        # Remove current ingredients from suggestions
        related_ingredients = related_ingredients - set(current_ingredients)
        
        # Sort by frequency
        suggestions = []
        for ingredient in related_ingredients:
            suggestions.append((ingredient, self.ingredient_frequencies[ingredient]))
        
        return [ingredient for ingredient, _ in sorted(suggestions, key=lambda x: x[1], reverse=True)[:top_n]]
    
    def find_similar_recipes(self, ingredients, top_n=3):
        """Find similar recipes based on ingredients"""
        if not self.recipes_data:
            return []
        
        # Create TF-IDF vectors for all recipes
        recipe_texts = [' '.join(recipe['ingredients']) for recipe in self.recipes_data]
        tfidf_matrix = self.vectorizer.fit_transform(recipe_texts)
        
        # Create vector for current ingredients
        current_text = ' '.join(ingredients)
        current_vector = self.vectorizer.transform([current_text])
        
        # Calculate similarity scores
        similarity_scores = cosine_similarity(current_vector, tfidf_matrix).flatten()
        
        # Get top similar recipes
        top_indices = similarity_scores.argsort()[-top_n:][::-1]
        
        return [self.recipes_data[i] for i in top_indices]

# Create a global instance
recommender = RecipeRecommender() 