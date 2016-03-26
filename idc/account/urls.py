from django.conf.urls import url, include

from account.views import UserProfileView, SSOAuthorizationView

urlpatterns = [
    url(r'profile/(?P<pk>\d+)/$', UserProfileView.as_view(), name='profile'),
    url(r'authorization/$', SSOAuthorizationView.as_view(), name='authorization'),
]
