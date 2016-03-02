import copy
import re

from django.contrib import admin, messages
from django.contrib.admin.options import csrf_protect_m
from django.db import models, transaction
from django.forms.widgets import Textarea
from django_mptt_admin.admin import DjangoMpttAdmin
from django_select2.forms import Select2TagWidget
from mptt.admin import MPTTModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from blog.utils import PostStatusTypes
from .models import Category, Comment, Post, Tag


class CategoryAdmin(DjangoMpttAdmin):
    tree_auto_open = False
    use_context_menu = True


def clean_html(raw_html):
    clean_regex = re.compile('<.*?>')
    clean_text = re.sub(clean_regex, '', raw_html)
    return clean_text


class PostAdmin(SimpleHistoryAdmin):
    list_display = ['__str__', 'author', 'modified_at', 'status', 'removed']
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

    def save_form(self, request, form, change):
        return super().save_form(request, form, change)

    def post_tags(self, post: Post):
        tags = post.tags.all().values_list('slug', flat=True)
        return ', '.join(tags)

    def save_model(self, request, obj: Post, form, change):
        if not obj.author:
            obj.author = request.user

        if not obj.excerpt:
            paragraph = clean_html(obj.content)
            obj.excerpt = paragraph[:min(len(paragraph) - 1, 256)]

        if (obj.pk and
                    Post.objects.get(pk=obj.pk).status != PostStatusTypes.PUBLISHED and
                    obj.status == PostStatusTypes.PUBLISHED and
                not request.user.is_superuser):
            obj.status = PostStatusTypes.REQUESTED
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

    @csrf_protect_m
    @transaction.atomic
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        categories = Category.objects.all()
        if not extra_context:
            extra_context = {}
        extra_context['categories'] = categories
        extra_context['status_options'] = PostStatusTypes.user_options()

        # This entire block is a dangerous hack. Please read it on your own risk
        if request.method == 'POST':

            tags = list(set(request.POST.getlist('tags')))[:5]  # type: List(str)
            original_tags = copy.deepcopy(tags)

            existing_tags = Tag.objects.all().filter(pk__in=[tag for tag in tags if tag.isdigit()])
            et_pk = [str(tag.pk) for tag in existing_tags]

            for tag in original_tags:
                if tag not in et_pk:
                    new_tag = Tag(slug=tag, created_by=request.user)
                    new_tag.save()
                    et_pk.append(str(new_tag.pk))

            request.POST = request.POST.copy()

            if len(et_pk) > 0:
                request.POST['tags'] = et_pk[0]
            for pk in et_pk[1:]:
                request.POST.update({
                    'tags': pk,
                })

        return super().changeform_view(request, object_id, form_url, extra_context)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(author=request.user)
        return queryset


class CommentAdmin(MPTTModelAdmin):
    list_display = ['comment', 'author', 'post']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(author=request.user)
        return qs


class TagAdmin(admin.ModelAdmin):
    list_display = ['slug', 'created_by', 'created_at']

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not request.user.is_superuser:
            fields.remove('created_by', 'created_at')
        return fields

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(created_by=request.user)
        return qs


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
