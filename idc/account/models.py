from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile')
    nickname = models.CharField(max_length=32)
    picture = models.ImageField(null=True, blank=True)
    cover = models.ImageField(null=True, blank=True)

    # Social Accounts
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    google = models.URLField(null=True, blank=True)
    blogger = models.URLField(null=True, blank=True)
    homepage = models.URLField(null=True, blank=True)
    behance = models.URLField(null=True, blank=True)
