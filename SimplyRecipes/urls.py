from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from recipe.views import IndexView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tags/", include("tag.urls")),
    path("recipes/", include("recipe.urls")),
    path("", IndexView.as_view(), name="index"),
]

if not settings.TESTING:
    urlpatterns = [
        *urlpatterns,
    ] + debug_toolbar_urls()
