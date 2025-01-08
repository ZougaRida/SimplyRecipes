from django.urls import path

from recipe import views

urlpatterns = [
    path("recipes/", views.RecipeListView.as_view(), name="recipe-list"),
    path(
        "recipes/<str:recipe>", views.RecipeDetailView.as_view(), name="recipe-detail"
    ),
    path("about/", views.AboutView.as_view(), name="about"),
]
