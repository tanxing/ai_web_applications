ingredients_detection_prompt = '''
Identify the food ingredients in this photo and provide a list in json format.

Example:
Input: A photo of the food inside a fridge
Output:
{
  "ingredients": ["apple", "banana", "bread", "butter", "cheese", "eggs", "mushrooms", "onion", "potato", "tomato"]
}
'''

recipe_suggestion_prompt = '''
You are a creative chef. Based on the following ingredients and retrieved recipes from my database, suggest 3 delicious and easy-to-make recipes. 

Ingredients Detected:
{ingredients}

Retrieved Recipes from Database:
{retrieved_recipes}

Please provide your suggestions in a clear, formatted way. Display the retrieved recipes first and then add more recipes to make up to 3 dishes.
'''
