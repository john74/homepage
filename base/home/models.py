from django.db import models


class SearchEngine(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=700)
    form_action = models.CharField(max_length=200)
    name_attribute = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.name
