from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.ForeignKey(User, related_name='user_profile')
    nickname = models.CharField(max_length=32)

    # Social Accounts
    facebook = models.URLField()
    twitter = models.URLField()
    behance = models.URLField()
