from django.db import models

from accounts.models import CustomUser

class SearchEngine(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=700)
    form_action = models.CharField(max_length=200)
    form_method = models.CharField(max_length=200)
    name_attribute = models.CharField(max_length=100)
    icon = models.URLField(max_length=500)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class BookmarkCategory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Bookmark Categories'

    def __str__(self):
        return self.name


class Bookmark(models.Model):
    category = models.ForeignKey(BookmarkCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=700)
    icon = models.URLField(max_length=500)
    shortcut = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Bookmarks'

    def __str__(self):
        return self.name
