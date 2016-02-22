from django.contrib import admin, messages
from django.db import models
from django.forms.widgets import Textarea
from django_mptt_admin.admin import DjangoMpttAdmin
from mptt.admin import MPTTModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from django_select2.forms import Select2TagWidget

from .models import Category, Comment, Post, Tag


class CategoryAdmin(DjangoMpttAdmin):
    tree_auto_open = False
    use_context_menu = True


class PostAdmin(SimpleHistoryAdmin):
    list_display = ['__str__', 'author', 'post_tags', 'created_at', 'modified_at', 'status', 'removed']
    list_filter = ['categories', 'status', 'removed']
    search_fields = ['title', 'excerpt', 'content', 'tags']
    list_editable = ['status', 'removed', ]

    date_hierarchy = 'modified_at'

    actions = ['move_to_trash', 'revive_posts']

    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={'rows': 3}),
        },
        models.ManyToManyField: {
            'widget': Select2TagWidget(
                attrs={
                    'data-width': '250px',
                    'data-maximum-selection-length': 5,
                }
            ),
        }
    }

    def post_tags(self, post: Post):
        tags = post.tags.all().values_list('name', flat=True)
        return ', '.join(tags)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        return super().save_model(request, obj, form, change)

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

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        categories = Category.objects.all()
        if not extra_context:
            extra_context = {}
        extra_context['categories'] = categories
        return super().changeform_view(request, object_id, form_url, extra_context)


class CommentAdmin(MPTTModelAdmin):
    list_display = ['comment', 'author', 'post']


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'slug', 'created_by', 'created_at']

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not request.user.is_superuser:
            fields.remove('created_by')
        return fields

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
