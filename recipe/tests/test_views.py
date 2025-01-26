from django.utils.http import urlencode

from django.test import TestCase
from django.core.paginator import Page
from django.urls import reverse

from recipe.models import Recipe
from tag.models import Tag


class TestIndexView(TestCase):
    @classmethod
    def setUpTestData(cls):
        tag = Tag.objects.create(name="Beef")
        tag.recipe_set.create(name="Beef1")
        tag.recipe_set.create(name="Beef2")
        tag.recipe_set.create(name="Beef3")

        Recipe.objects.bulk_create([Recipe(name=f"Recipe{i}") for i in range(1, 21)])

    def test_view_in_normal_conditions(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipe/index.html")
        query_recipes = response.context.get("ingredients_list_pagination")
        self.assertIsInstance(query_recipes, Page)

        # check that pagination is working as expected
        self.assertQuerySetEqual(Recipe.objects.all()[:12], query_recipes)

    def test_view_with_parameters(self):
        response = self.client.get("/?tag=Beef")
        self.assertEqual(response.status_code, 200)
        # Note we are not testing for HTMX behavior at all for now.
        self.assertTemplateUsed(response, "recipe/index.html")
        self.assertQuerysetEqual(
            Recipe.objects.filter(tags__name="Beef"),
            response.context.get("ingredients_list_pagination"),
        )

        response = self.client.get("/?tag=Beef&page=3")
        self.assertEqual(response.status_code, 200)


class TestRecipeDetailView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.recipe = Recipe.objects.get("French Fries")

    def test_available_recipe(self):
        response = self.client.get(self.recipe.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipe/recipe_detail.html")
        self.assertEqual(response.context.get("recipe"), self.recipe)

    def test_unavailable_recipe(self):
        response = self.client.get("recipes/Chicken-Sandwich/")
        self.assertEqual(response.status_code, 404)

        response = self.client.get("/recipe/2")
        self.assertEqual(response.status_code, 404)

        response = self.client.get("/some-random-recipe-name/")
        self.assertEqual(response.status_code, 404)


class TestRecipeListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.main_dish = Recipe.objects.create(name="Delicious Soup Dish")
        Recipe.objects.create(name="Chicken")
        cls.dish = Recipe.objects.create(name="Fish Dish")

    def test_no_parameters(self):
        response = self.client.get(reverse("recipe-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipe/recipe_list.html")

        # make sure pagination still works
        self.assertTrue(response.context.get("is_paginated"))

        self.assertQuerysetEqual(
            Recipe.objects.all()[:12], response.context.get("recipe_list_pagination")
        )

    def test_with_parameters(self):
        response = self.client.get(
            f"{reverse('recipe_list')}?{urlencode({'query': 'dish'})}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipe/recipe_list.html")
        self.assertTrue(response.context.get("is_paginated"))

        # the recipes are ordered alphabetically of course to ensure pagination
        self.assertListEqual(response.context.get("recipe_list_pagination"), [self.main_dish, self.dish])

        response = self.client.get(
            f"{reverse('recipe_list')}?{urlencode({'query': ''})}"
        )
        self.assertQuerysetEqual(Recipe.objects.all()[:12], response.context.get("recipe_list_pagination"))


    def test_no_query_matched(self):
        response = self.client.get(
            f"{reverse('recipe_list')}?{urlencode({'query': 'some random nonsense'})}"
        )

        self.assertEqual(response.status_code, 404)