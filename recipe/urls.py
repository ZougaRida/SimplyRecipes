from django.urls import path

from recipe import views

urlpatterns = [
    path("", views.RecipeListView.as_view(), name="recipe-list"),
    path(
        "<str:recipe>", views.RecipeDetailView.as_view(), name="recipe-detail"
    ),
]
