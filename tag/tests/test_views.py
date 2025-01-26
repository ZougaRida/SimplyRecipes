from django.test import TestCase
from django.urls import reverse

from tag.models import Tag
from recipe.models import Recipe


class TestDetailViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tag = Tag.objects.create(name="Dinner")
        cls.tag.recipe_set.create(name="Chips")
        cls.tag.recipe_set.create(name="Boiled Eggs")
        cls.tag.recipe_set.create(name="Soup")

    def test_existing_tag(self):
        response = self.client.get(reverse("tag-detail", args=[self.tag]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tag/tag_detail.html")
        self.assertTrue(response.context.get("is_paginated"))

        self.assertQuerysetEqual(self.tag.recipe_set.all()[:12], response.context.get("recipe_list_pagination"))


    def test_non_existing_tag(self):
        response = self.client.get(reverse("tag-detail", args=["random-tag"]))
        self.assertEqual(response.status_code, 404)


class TestTagListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tag1 = Tag.objects.create(name="Dinner")
        cls.tag1.recipe_set.create(name="Dinner1")
        cls.tag1.recipe_set.create(name="Dinner2")
        cls.tag1.recipe_set.create(name="Dinner3")
        cls.tag1.recipe_set.create(name="Dinner4")
        cls.tag1.recipe_set.create(name="Dinner5")

        cls.tag2 = Tag.objects.create(name="Breakfast")
        cls.tag1.recipe_set.create(name="Breakfast1")
        cls.tag1.recipe_set.create(name="Breakfast2")
        cls.tag1.recipe_set.create(name="Breakfast3")
        cls.tag1.recipe_set.create(name="Breakfast4")
        cls.tag1.recipe_set.create(name="Breakfast5")
        cls.tag1.recipe_set.create(name="Breakfast6")
        cls.tag1.recipe_set.create(name="Breakfast7")
        Recipe.objects.create(name="Breakfast8")
        Recipe.objects.create(name="Breakfast9")
        Recipe.objects.create(name="Breakfast10")


    def test_view(self):
        response = self.client.get(reverse("tag-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tag/tag_list.html")
        self.assertQuerySetEqual(response.context.get("tag_list"), [self.tag1, self.tag2], ordered=False)
        self.assertEqual(self.tag1.recipe__count, 5)
        self.assertEqual(self.tag2.recipe__count, 7)