from django.contrib import admin
from .models import Interface, Profile, Email, ApiKey, Theme


admin.site.register(Interface)
admin.site.register(Profile)
admin.site.register(Email)
admin.site.register(ApiKey)
admin.site.register(Theme)
