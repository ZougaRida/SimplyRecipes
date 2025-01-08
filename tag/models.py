from django.db import models
from django.shortcuts import reverse


class Tag(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def get_absolute_url(self):
        return reverse("tag-detail", kwargs={"pk": self.name})

    def __str__(self):
        return self.name
