from django.db import models

from accounts.models import CustomUser

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
