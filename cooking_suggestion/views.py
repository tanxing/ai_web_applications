from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from google import genai
from google.genai import types
from sentence_transformers import SentenceTransformer, util
from .prompts.gemini_prompts import ingredients_detection_prompt, recipe_suggestion_prompt
import json
import re
from .models import Recipe

def home(request):
  return render(request, 'home.html')

def cooking_suggestion(request):
  template = loader.get_template('main_ui.html')
  return HttpResponse(template.render({}, request))

def parse_gemini_output(text: str):
  # Strip leading/trailing whitespace
  cleaned = text.strip().lower()

  # Remove leading and trailing triple backticks (optional)
  cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
  cleaned = re.sub(r"\s*```$", "", cleaned)

  # Now `cleaned` should contain pure JSON
  return json.loads(cleaned)

def retrieve_recipes(ingredient_list: list[str]):
  # Load model
  model = SentenceTransformer('all-MiniLM-L6-v2')
    
  # Get all recipes that have embeddings
  recipes = Recipe.objects.exclude(ingredient1_embedding__isnull=True).exclude(ingredient1_embedding=[])
    
  if not recipes.exists() or not ingredient_list:
    return []

  # Encode detected ingredients
  ingredient_embeddings = model.encode(ingredient_list)
    
  # Store results
  results = []
  threshold = 0.8
    
  for r in recipes:
    recipe_embedding = r.ingredient1_embedding
    # Calculate cosine similarity for each detected ingredient
    similarities = util.cos_sim(ingredient_embeddings, recipe_embedding)
        
    # Get the max similarity for this recipe against any detected ingredient
    max_sim = float(similarities.max())
    print(r.name, r.ingredient1, max_sim)
        
    if max_sim >= threshold:
      results.append({
        'name': r.name,
        'description': r.description,
        'instructions': r.instructions,
        'similarity': max_sim
      })
    
  # Sort by similarity
  results.sort(key=lambda x: x['similarity'], reverse=True)
  return results

def gemini_inference(request):
  if request.method == 'POST' and request.FILES.get('food_photo'):
    food_photo = request.FILES['food_photo']

    # Configure Gemini Client
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    # Prepare image data
    image_data = food_photo.read()

    prompt = ingredients_detection_prompt

    try:
      response = client.models.generate_content(
        model='gemini-3-flash-preview',
        contents=[
          prompt,
          types.Part.from_bytes(data=image_data, mime_type=food_photo.content_type)
        ]
      )
      text_output = response.text
      parsed_output = parse_gemini_output(text_output)
      ingredient_list = parsed_output['ingredients']

      # Match ingredients against local database
      retrieved_recipes = retrieve_recipes(ingredient_list)

      # RAG: Format the recipe suggestion prompt with retrieved data
      formatted_recipe_prompt = recipe_suggestion_prompt.format(
          ingredients=", ".join(ingredient_list),
          retrieved_recipes=json.dumps(retrieved_recipes, indent=2)
      )

      response = client.models.generate_content(
        model='gemini-3-flash-preview',
        contents=[formatted_recipe_prompt]
      )
      suggested_recipes = response.text

      context = {
        'text_output': text_output,
        'ingredients': ingredient_list,
        'retrieved_recipes': retrieved_recipes,
        'suggested_recipes': suggested_recipes
      }
    except Exception as e:
      context = {
        'ingredients': "Error",
        'suggestions': f"Could not analyze image: {str(e)}",
      }
    
    return render(request, 'main_ui.html', context)
    
  return cooking_suggestion(request)