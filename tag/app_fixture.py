import requests
import django
import os

# Please note that the 2 lines SHOULD COME before importing the Tag model.
# Otherwise, an error will be thrown.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SimplyRecipes.settings")
django.setup()

from tag.models import Tag

response = requests.get("https://www.themealdb.com/api/json/v1/1/categories.php")
if response.status_code == 200:
    categories_list = response.json()["categories"]
    categories_entries = [Tag(category["strCategory"]) for category in categories_list]
    Tag.objects.bulk_create(categories_entries)
    print("Categories created successfully.")