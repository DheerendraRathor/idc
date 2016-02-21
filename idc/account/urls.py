from django.conf.urls import url, include

from account.views import UserProfileView

urlpatterns = [
    url(r'profile/(?P<pk>\d+)/$', UserProfileView.as_view(), name='profile'),
]
