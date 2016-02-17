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
