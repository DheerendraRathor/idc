from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.generic import TemplateView, View
from oauth.authorization import Authorization
from oauth.exceptions import OAuthError
from oauth.models import OAuthToken
from oauth.request import UserFieldAPIRequest, OAuthObject


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


class SSOAuthorizationView(View):

    def get(self, request):
        if request.user.is_authenticated():
            if request.GET.get('next') != '' and request.GET.get('next') is not None:
                return redirect(request.GET.get('next'))
            else:
                return redirect(settings.LOGIN_REDIRECT_URL)
        try:
            token = Authorization(request).get_token()
        except OAuthError as e:
            return render(request, 'login.html', {'error': e.message, 'client_id': settings.CLIENT_ID})

        if not token:
            return render(request, 'login.html', {'client_id': settings.CLIENT_ID})

        user_data = UserFieldAPIRequest(
            fields=[
                'id',
                'first_name',
                'last_name',
                'email',
                'username',
            ],
            token=token
        )

        user_obj = OAuthObject(user_data)

        user, created = User.objects.get_or_create(username=user_data.username)
        user.set_unusable_password()

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth.login(request, user)

        if request.GET.get('state') != '' and request.GET.get('state') is not None:
            return redirect(request.GET.get('state'))
        else:
            return redirect(settings.LOGIN_REDIRECT_URL)
