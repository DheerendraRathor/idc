from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, related_name='user_profile')
    nickname = models.CharField(max_length=32)

    # Social Accounts
    facebook = models.URLField()
    twitter = models.URLField()
    behance = models.URLField()
