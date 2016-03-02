from django.shortcuts import get_object_or_404
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

        post.increment_views()

        kwargs['post'] = post
        return super().get(request, *args, **kwargs)

class BlogPostsView(TemplateView):
    RECENT = 1
    TOP = 2

    template_name = 'blog/blogs.html'

    def get(self, request, *args, **kwargs):
        option = kwargs.pop('option', self.RECENT)
        count = kwargs.pop('count', 12)

        if option == self.RECENT:
            posts = Post.objects.order_by('-created_at')[:count]
        elif option == self.TOP:
            posts = Post.objects.order_by('-views')[:count]
        else:
            posts = Post.objects.all()[:count]

        top_post = posts[0]
        top_post.increment_views()

        kwargs['post'] = top_post
        kwargs['posts'] = posts[1:]

        return super().get(request, *args, **kwargs)
