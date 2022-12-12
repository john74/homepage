from django.contrib import admin
from .models import SearchEngine, BookmarkCategory, Bookmark, ApiKey


admin.site.register(SearchEngine)
admin.site.register(BookmarkCategory)
admin.site.register(Bookmark)
admin.site.register(ApiKey)
