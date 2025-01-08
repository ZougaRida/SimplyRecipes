from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.views.generic import DetailView, ListView, TemplateView

from recipe.models import Recipe, RecipeIngredient
from tag.models import Tag


class IndexView(TemplateView):
    """
    The Index View takes care of mainly showing off all recipes and filtering them based on tags.

    This View uses HTMX for 2 main purposes:
    * Infinite Scroll by paginating behind the scenes and issuing a GET request when a certain condition is satisfied to
    add additional recipes.
    * Filtering recipes by tag and of course still maintain the infinite scroll effect.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tag = self.request.GET.get("tag")

        if tag:
            recipe_list = Recipe.objects.filter(tags__name=tag)
            # If tag was sent as a parameter, then this came from filtering based on tag
            # with the help of HTMX, thus the url to point to for pagination changes too.
        else:
            # Of course, if no tag was sent as a parameter, then either this request was made
            # without HTMX or using the "All" button with HTMX, either case we need to get the entire list
            # of recipes and paginate of course to make infinite scroll effect.
            # the pagination link in this case will be the usual index without any tag as parameter
            recipe_list = Recipe.objects.all()

        # this is just to make sure that we only fetch the following fields from the database.
        recipe_list = recipe_list.only(
            "name", "image_url", "preparation_time", "cooking_time"
        )

        # Simple pagination logic.
        paginator = Paginator(recipe_list, 12)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj

        # Of course, if the request was not issued with the help of HTMX,
        # then we need to render the entire page, and thus we will need to fetch tags from database
        # the HX-Request header is true when using HTMX
        # otherwise it's None since it doesn't exist in headers if the request was issued without HTMX.
        if self.request.headers.get("HX-Request") is None:
            context["tag_list"] = Tag.objects.all()

        return context

    def get_template_names(self):
        """Chooses whether to render entire index template or only the recipes-grid partial if request was
        issued using HTMX."""

        if self.request.headers.get("HX-Request"):
            template_name = "recipe/components/recipe-grid.html"
        else:
            template_name = "recipe/index.html"

        return template_name


class RecipeListView(ListView):
    """
    This View is highly important featuring the active search.

    This View can be called either with GET or POST requests.
    for GET requests, it will display all recipes with infinite scroll effect.
    for POST requests, it will filter the recipes based on the search query and still maintain the infinite scroll effect.
    """

    paginate_by = 12

    def get_queryset(self):
        """the code self explains itself."""
        query = self.request.GET.get("query")

        if query:
            recipes = Recipe.objects.filter(name__icontains=query)
        else:
            recipes = Recipe.objects.all()

        return recipes.only("name", "image_url", "preparation_time", "cooking_time")

    def get_template_names(self):
        """Same logic as Index View template choosing."""
        if self.request.headers.get("HX-Request"):
            template_name = "recipe/components/recipe-grid.html"
        else:
            template_name = "recipe/recipe_list.html"

        return template_name


class RecipeDetailView(DetailView):
    def get_object(self, **kwargs):
        recipe = self.kwargs.get("recipe").replace("-", " ")
        return Recipe.objects.prefetch_related(
            Prefetch(
                "ingredients",
                queryset=RecipeIngredient.objects.select_related("ingredient").defer(
                    "recipe"
                ),
                to_attr="recipe_ingredients",
            )
            # here for each record in RecipeIngredient we are getting the ingredient model along with it too,
            # though without hitting the database for each ingredient.
            # the defer method is just to get rid of at least the recipe_id field
            # I can't get rid of primary_id since defer doesn't allow that,
            # nor unfortunately the ingredient_id column which is simply a replica of ingredient_name column
        ).get(name=recipe)


class AboutView(ListView):
    template_name = "recipe/about.html"

    def get_queryset(self):
        return Recipe.objects.order_by("?").only(
            "name", "image_url", "preparation_time", "cooking_time"
        )[:3]
