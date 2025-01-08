from django.urls import path

from tag import views

urlpatterns = [
    path("", views.TagListView.as_view(), name="tag-list"),
    path("<str:tag>/", views.TagDetailView.as_view(), name="tag-detail"),
]
