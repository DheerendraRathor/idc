from django.conf.urls import url, include

from blog.views import BlogPostView

urlpatterns = [
    url(r'post/(?P<pk>\d+)/$', BlogPostView.as_view(), name='post'),
]
