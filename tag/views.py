from django.db.models import Count
from django.views.generic import ListView

from recipe.models import Recipe
from tag.models import Tag


class TagListView(ListView):
    queryset = Tag.objects.annotate(Count("recipe"))


class TagDetailView(ListView):
    """
    This View uses the recipes-grid, and of course the pagination logic or rather infinite scroll effect is still
    maintained.
    """

    allow_empty = False
    paginate_by = 12

    def get_queryset(self):
        tag = self.kwargs["tag"]
        return Recipe.objects.filter(tags__name=tag).only(
            "name", "image_url", "preparation_time", "cooking_time"
        )

    def get_template_names(self):
        """
        Same as IndexView, based on whether the request was issued with HTMX or not, the template
        to render changes accordingly; either the entire template or only the recipes-grid.
        """

        if self.request.headers.get("HX-Request"):
            template_name = "recipe/components/recipe-grid.html"
        else:
            template_name = "tag/tag_detail.html"

        return template_name

    def get_context_data(self, **kwargs):
        """Change that page_obj name to something meaningful."""

        context = super().get_context_data(**kwargs)
        context["recipe_list_pagination"] = context.pop("page_obj")
        return context
