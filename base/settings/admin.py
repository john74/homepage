from django.contrib import admin
from .models import Interface, Profile, Email, ApiKey


admin.site.register(Interface)
admin.site.register(Profile)
admin.site.register(Email)
admin.site.register(ApiKey)
