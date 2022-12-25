from django.contrib import admin
from .models import Interface, Profile, EmailService, Email, ApiKey


admin.site.register(Interface)
admin.site.register(Profile)
admin.site.register(EmailService)
admin.site.register(Email)
admin.site.register(ApiKey)
