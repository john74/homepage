from django.contrib import admin
from .models import SearchEngine, EmailService, ApiService


admin.site.register(SearchEngine)
admin.site.register(EmailService)
admin.site.register(ApiService)
