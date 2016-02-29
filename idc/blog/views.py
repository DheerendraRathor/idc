from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from blog.models import Post


class BlogPostView(TemplateView):

    template_name = 'blog/post.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        post = get_object_or_404(
            Post,
            pk=pk
        )
        kwargs['post'] = post
        return super().get(request, *args, **kwargs)


class BlogPostsView(TemplateView):

    PUBLIC = 1
    PRIVATE = 2
    BOTH = 3

    RECENT = 1

    template_name = 'blog/blogs.html'

    def get(self, request, *args, **kwargs):
        option = kwargs.pop('option', self.RECENT)
        view = kwargs.pop('view', self.BOTH)
        posts = Post.objects.order_by('-created_at')[:10]
        kwargs['posts'] = posts
        return super().get(request, *args, **kwargs)