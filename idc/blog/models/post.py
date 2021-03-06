from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from froala_editor.fields import FroalaField
from simple_history.models import HistoricalRecords

from .category import Category
from .tag import Tag
from ..utils import PostStatusTypes


class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True)
    cover_image = models.ImageField(upload_to='post', null=True, blank=True)
    title = models.TextField(help_text='Title of post')
    content = FroalaField()
    excerpt = models.TextField(help_text='Custom intro or short version of the content', null=True, blank=True)
    status = models.IntegerField(choices=PostStatusTypes.choices(), default=PostStatusTypes.DRAFT, blank=True,
                                 null=True)
    comments_allowed = models.BooleanField(default=True, help_text='If comments are allowed')
    categories = models.ManyToManyField(Category, related_name='posts', blank=True, db_index=True)
    removed = models.BooleanField(default=False, help_text='Temporarily remove post')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    history = HistoricalRecords()
    views = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return (self.title[:50] + '...') if len(self.title) > 50 else self.title

    def get_absolute_url(self):
        url = reverse('blog:post', args=[self.id, ])
        return url

    def increment_views(self):
        if not self.views:
            self.views = 0
        self.views = self.views + 1
        self.save()
