from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from froala_editor.fields import FroalaField
from mptt.models import MPTTModel, TreeForeignKey
from simple_history.models import HistoricalRecords

from .utils import PostStatusTypes


class Category(MPTTModel):
    name = models.CharField(max_length=64)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE,
                            db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    cover_image = models.ImageField(upload_to='post', null=True, blank=True)
    title = models.TextField(help_text='Title of post')
    content = FroalaField()
    excerpt = models.TextField(help_text='Custom intro or short version of the content', null=True, blank=True)
    status = models.IntegerField(choices=PostStatusTypes.choices(), default=PostStatusTypes.DRAFT)
    comments_allowed = models.BooleanField(default=True, help_text='If comments are allowed')
    categories = models.ManyToManyField(Category, related_name='posts', blank=True, db_index=True)
    removed = models.BooleanField(default=False, help_text='Temporarily remove post')
    tags = ArrayField(base_field=models.SlugField(max_length=32), size=10, null=True, blank=True,
                      help_text='Comma separated list of tags', db_index=True)
    history = HistoricalRecords()

    def __str__(self):
        return (self.title[:50] + '...') if len(self.title) > 50 else self.title


class Comment(MPTTModel):
    author = models.ForeignKey(User, related_name='comments')
    post = models.ForeignKey(Post, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    def __str__(self):
        return self.comment
