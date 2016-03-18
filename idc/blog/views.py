from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from blog.forms import CommentForm
from blog.models import Post, Comment
from blog.utils import PostStatusTypes


class BlogPostView(TemplateView):
    template_name = 'blog/post.html'

    def get_post(self, **kwargs):
        pk = kwargs.pop('pk', None)
        post = get_object_or_404(
                Post,
                pk=pk
        )
        return post

    def get(self, request, *args, **kwargs):

        post = self.get_post(**kwargs)
        if post.status == PostStatusTypes.DRAFT or (not request.user.is_authenticated()
                                                    and post.status != PostStatusTypes.PUBLISHED):
            raise Http404

        post.increment_views()

        comment_form = CommentForm()
        comments = Comment.objects.all().filter(post=post)

        kwargs['post'] = post
        kwargs['comment_form'] = comment_form
        kwargs['comments'] = comments

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = Comment()
            comment.author = request.user
            comment.comment = comment_form.cleaned_data['comment']
            comment.post = self.get_post(**kwargs)
            comment.save()
            return self.get(request, *args, **kwargs)
        else:
            return self.get(request, *args, **kwargs)

class BlogPostsView(TemplateView):
    RECENT = 1
    TOP = 2

    template_name = 'blog/blogs.html'

    def get(self, request, *args, **kwargs):
        option = kwargs.pop('option', self.RECENT)
        count = kwargs.pop('count', 12)

        posts = Post.objects.exclude(status=PostStatusTypes.DRAFT)

        if not request.user.is_authenticated():
            posts = posts.filter(status=PostStatusTypes.PUBLISHED)

        if option == self.RECENT:
            posts = posts.order_by('-created_at')[:count]
        elif option == self.TOP:
            posts = posts.order_by('-views')[:count]
        else:
            posts = posts[:count]

        top_post = posts[0]
        top_post.increment_views()

        kwargs['post'] = top_post
        kwargs['posts'] = posts[:]

        return super().get(request, *args, **kwargs)
