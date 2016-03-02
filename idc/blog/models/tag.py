from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    slug = models.SlugField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='tags')

    def __str__(self):
        return self.slug
