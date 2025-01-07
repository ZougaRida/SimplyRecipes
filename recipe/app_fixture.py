import os

import django
import requests
from django.db import transaction

# Please note that the 2 lines SHOULD COME before importing the models.
# Otherwise, an error will be thrown.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SimplyRecipes.settings")
django.setup()

from recipe.models import Recipe, Tool, RecipeIngredient, Ingredient

# First, we will create the Tool instances.
# Please note that this will be a list of default tools.
# Further instances will be created later through the admin page.
cooking_tools = [
    "Chef's Knife",
    "Cutting Board",
    "Measuring Cups and Spoons",
    "Mixing Bowls",
    "Wooden Spoon or Spatula",
    "Whisk",
    "Colander",
    "Frying Pan/Skillet",
    "Saucepan",
    "Baking Sheet/Tray",
]

Tool.objects.bulk_create([Tool(tool) for tool in cooking_tools])

# Next we'll create the Ingredient instances
response = requests.get("https://www.themealdb.com/api/json/v1/1/list.php?i=list")
generic_ingredient_image_url = (
    "https://www.themealdb.com/images/ingredients/{name}-Small.png"
)
if response.status_code == 200:
    ingredients = response.json()["meals"]
    Ingredient.objects.bulk_create(
        [
            Ingredient(
                name=ingredient["strIngredient"],
                image_url=generic_ingredient_image_url.format(
                    name=ingredient["strIngredient"]
                ),
            )
            for ingredient in ingredients
        ]
    )

# Onward to the big beast, creating the Recipe instances.
# First, the transaction.atomic context manager makes sure that if an Exception is raised,
# the entire previous successful saves to the database are aborted,
# thus either everything passes through to the database or nothing at all.
with transaction.atomic():
    # Now time to create the recipes
    base_url = "https://www.themealdb.com/api/json/v1/1/search.php?f="

    for letter in "abcdefghijklmnopqrstuvwxyz":
        response = requests.get(base_url + letter)
        if response.status_code == 200:
            recipes = response.json()["meals"]
            if recipes is not None:
                Recipe.objects.bulk_create(
                    Recipe(
                        name=recipe["strMeal"],
                        instructions=recipe["strInstructions"].replace("\r", ""),
                        image_url=recipe["strMealThumb"],
                    )
                    for recipe in recipes
                )

                # Normally, a recipe could have many Tags like (Dinner, Spicy)
                # though the API only returns one main Tag for each Recipe.
                # Thus, we'll content on it for now, but further tags for each recipe will be added later.
                for recipe in recipes:
                    recipe_instance = Recipe.objects.get(name=recipe["strMeal"])
                    recipe_instance.tags.add(recipe["strCategory"])

                # Finally, for each recipe we take its list of ingredients,
                # and for each ingredient save the quantity used.

                for recipe in recipes:
                    i = 1
                    while (
                            recipe[f"strIngredient{i}"] is not None
                            and recipe[f"strIngredient{i}"] != ""
                    ):
                        # There seems to be some ingredients that are used and weren't saved previously when saving
                        # all ingredient instances. Thus, we have to get or create them if not existing in Ingredient
                        # Table and keep noting them since some ARE SIMPLY typos or Capitalization errors.
                        # To note them or rather distinguish them from previous ingredients created at the top,
                        # the image_url will be empty for the ones created here.
                        ingredient, created = Ingredient.objects.get_or_create(
                            name=recipe[f"strIngredient{i}"]
                        )

                        RecipeIngredient.objects.create(
                            recipe_id=recipe["strMeal"],
                            ingredient=ingredient,
                            quantity=recipe[f"strMeasure{i}"],
                        )

                        i += 1

                        # 20 is the maximum value that the counter can take in the API response.
                        if i == 20:
                            break

    # now that we created all recipe instances, for each recipe,
    # we need to add the default list of tools
    recipe_instances = Recipe.objects.all()
    # the add method of ManytoMany relationship accepts either instances or primary keys
    for recipe_instance in recipe_instances:
        recipe_instance.tools.add(*cooking_tools)

print("Finally, Database fixture through API is successful.")
