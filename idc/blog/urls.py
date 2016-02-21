from django.conf.urls import url, include

from blog.views import BlogPostView, BlogPostsView

urlpatterns = [
    url(r'post/(?P<pk>\d+)/$', BlogPostView.as_view(), name='post'),
    url(r'posts/', BlogPostsView.as_view(), name='post'),
    url(r'posts/(?P<option>\d+)/$', BlogPostsView.as_view(), name='post'),
    url(r'posts/(?P<option>\d+)/(?P<view>\d+)/$', BlogPostsView.as_view(), name='post'),
]
