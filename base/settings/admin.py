from django.contrib import admin
from .models import Interface, Profile, EmailService, Email, Api, Theme


admin.site.register(Interface)
admin.site.register(Profile)
admin.site.register(EmailService)
admin.site.register(Email)
admin.site.register(Api)
admin.site.register(Theme)
