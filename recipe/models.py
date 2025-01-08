from django.db import models
from django.urls import reverse

from tag.models import Tag

# A default description to all recipes still not modified yet.

default_description = (
    "This is a default description to the Recipe. Since TheMealDB API doesn't specify a lot of "
    "details to the recipes (description, cooking time, preparation time and number of servings), "
    "this one was made until it will be fixed manually later."
)


class Recipe(models.Model):
    name = models.CharField(max_length=150, primary_key=True)
    instructions = models.TextField()
    image_url = models.URLField()

    # The following 4 attributes of Recipe are not specified
    # when using the "TheMealDB" API, thus will be given a default value for now.
    # Though, they will be updated regularly through the Admin App once deployed.
    preparation_time = models.PositiveSmallIntegerField(default=10)
    cooking_time = models.PositiveSmallIntegerField(default=20)
    number_of_servings = models.PositiveSmallIntegerField(default=4)
    description = models.TextField(default=default_description)

    # Since we're updating the above 4 attributes regularly later,
    # these 2 attributes will help to distinguish between the updated recipes
    # and the ones who still aren't.
    last_modified = models.DateField(auto_now=True)
    has_been_updated = models.BooleanField(default=False)

    tools = models.ManyToManyField("Tool")
    ingredients = models.ManyToManyField("Ingredient", through="RecipeIngredient")
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

    @property
    def instructions_list(self):
        return self.instructions.split("\n")

    def get_absolute_url(self):
        # The reason for replacing spaces in recipe names so that
        # the display of url would not be bad looking.
        # For example, if "Banana Pancakes" was sent as keyword in url, its display will be
        # "Banana%20Pancakes" which is not a good-looking url.
        return reverse(
            "recipe-detail",
            kwargs={"recipe": self.name.replace(" ", "-")},
        )

    class Meta:
        """Important for pagination logic, this makes sure to order recipes by ascending order."""

        ordering = ["name"]


class Ingredient(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    image_url = models.URLField()

    def __str__(self):
        return self.name


class Tool(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """
    Important model that serves as intermediary of ManytoMany between Recipe and Ingredient models.
    The reason for it is to store for each relationship the quantity of that ingredient in that recipe.

    """

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=75)
