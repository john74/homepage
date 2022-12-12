from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#custom-users-and-django-contrib-admin
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "password"]

    # fields to be used in editing users
    fieldsets = (
        (None, {'fields': ('email', 'password', 'country', 'city')}),
    )

    # fields to be used when creating users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'country', 'city')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.unregister(Group)
