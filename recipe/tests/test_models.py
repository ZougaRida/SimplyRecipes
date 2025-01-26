from django.db.utils import IntegrityError
from django.test import TransactionTestCase
from psycopg.errors import UniqueViolation

from recipe.models import Recipe


class TestRecipe(TransactionTestCase):
    def test_recipe_model(self):
        recipe1 = Recipe.objects.create(name="Apple Pie")

        # test the __str__ method
        self.assertEqual(str(recipe1), "Apple Pie")

        # test the default values
        self.assertEqual(recipe1.preparation_time, 10)
        self.assertEqual(recipe1.cooking_time, 20)
        self.assertEqual(recipe1.number_of_servings, 4)
        self.assertFalse(recipe1.has_been_updated)

        # change some values to test them
        recipe1.instructions = "Step1\nStep2\nStep3\nEnd"
        recipe1.has_been_updated = True

        recipe1.save()
        self.assertTrue(recipe1.has_been_updated)
        self.assertListEqual(
            recipe1.instructions_list, ["Step1", "Step2", "Step3", "End"]
        )

        # test the recipe get_absolute_url method
        self.assertURLEqual(recipe1.get_absolute_url(), "/recipes/Apple-Pie/")

        # test that no recipe with same name can be created since name is primary key
        with self.assertRaises(IntegrityError):
            Recipe.objects.create(name="Apple Pie")

        # test the IngredientRecipe Model and check everything is working properly
        recipe1.ingredients.create(name="Apple", through_defaults={"quantity": "1 Kg"})
        recipe1.ingredients.create(
            name="Flour", through_defaults={"quantity": "1.5 Kg"}
        )

        self.assertQuerySetEqual(
            recipe1.ingredients.all(), ["Apple", "Flour"], transform=str ,ordered=False
        )
        self.assertQuerySetEqual(
            recipe1.recipeingredient_set.values_list("quantity", flat=True),
            ["1 Kg", "1.5 Kg"],
            ordered=False,
        )


