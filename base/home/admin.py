from django.contrib import admin
from .models import SearchEngine, BookmarkCategory, Bookmark


admin.site.register(SearchEngine)
admin.site.register(BookmarkCategory)
admin.site.register(Bookmark)
