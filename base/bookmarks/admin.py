from django.contrib import admin
from .models import BookmarkCategory, BookmarkSubCategory, Bookmark


admin.site.register(BookmarkCategory)
admin.site.register(BookmarkSubCategory)
admin.site.register(Bookmark)
