"""idc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import re

import froala_editor.urls
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve

import account.urls
import blog.urls

from .views import IndexView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/blog/posts/'}),
    url(r'^blog/', include(blog.urls, namespace='blog')),
    url(r'^account/', include(account.urls, namespace='account')),
    url(r'^froala_editor/', include(froala_editor.urls)),
]

urlpatterns += [
    url(r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')), serve,
        kwargs={'document_root': settings.STATIC_ROOT}),
    url(r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')), serve,
        kwargs={'document_root': settings.MEDIA_ROOT}),
]
