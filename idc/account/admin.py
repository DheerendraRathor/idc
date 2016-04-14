from django.contrib import admin

from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):

    exclude = ['user']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(user=request.user)
        return qs


admin.site.register(UserProfile, UserProfileAdmin)
