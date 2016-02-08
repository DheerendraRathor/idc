from django.contrib import admin, messages
from django.db import models
from django.forms.widgets import Textarea
from django_mptt_admin.admin import DjangoMpttAdmin
from mptt.admin import MPTTModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from .models import Category, Comment, Post


class CategoryAdmin(DjangoMpttAdmin):
    tree_auto_open = False
    use_context_menu = True


class PostAdmin(SimpleHistoryAdmin):
    list_display = ['__str__', 'author', 'post_tags', 'created_at', 'modified_at', 'status', 'removed']
    list_filter = ['categories', 'status', 'removed']
    search_fields = ['title', 'excerpt', 'content', 'tags']

    date_hierarchy = 'modified_at'

    actions = ['move_to_trash', 'revive_posts']

    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={'rows': 3})
        }
    }

    def post_tags(self, post: Post):
        return ', '.join(post.tags)

    def move_to_trash(self, request, queryset):
        posts_deleted = queryset.update(removed=True)
        if posts_deleted == 1:
            message_bit = '1 post is'
        else:
            message_bit = '%d posts are' % posts_deleted
        messages.add_message(request, messages.SUCCESS, '%s moved to trash' % message_bit)

    def revive_posts(self, request, queryset):
        posts_revived = queryset.update(removed=False)
        if posts_revived == 1:
            message_bit = '1 post is'
        else:
            message_bit = '%d posts are' % posts_revived
        messages.add_message(request, messages.SUCCESS, '%s recovered successfully' % message_bit)

    move_to_trash.short_description = 'Move posts to recycle bin'
    revive_posts.short_description = 'Recover posts from recycle bin'


class CommentAdmin(MPTTModelAdmin):
    list_display = ['comment', 'author', 'post']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
