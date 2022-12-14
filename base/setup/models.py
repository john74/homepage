from django.db import models
from accounts.models import CustomUser


class SearchEngine(models.Model):
    name = models.CharField(max_length=100, unique=True)
    url = models.CharField(max_length=700)
    form_action = models.CharField(max_length=200)
    form_method = models.CharField(max_length=200)
    name_attribute = models.CharField(max_length=100)
    icon = models.URLField(max_length=500)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class EmailService(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, unique=True)

    class Meta:
        verbose_name_plural = 'Email Services'

    def __str__(self):
        return self.name


class ApiService(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, unique=True)

    class Meta:
        verbose_name_plural = 'Api Services'

    def __str__(self):
        return self.name
