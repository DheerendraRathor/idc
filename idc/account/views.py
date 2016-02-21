from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import TemplateView


class UserProfileView(TemplateView):
    template_name = 'profile/profile.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        user = get_object_or_404(
                User,
                pk=pk
        )

        kwargs['user'] = user
        return super().get(request, *args, **kwargs)
