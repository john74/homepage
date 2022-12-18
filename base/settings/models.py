from django.db import models
from accounts.models import CustomUser


class Interface(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    theme_light = models.BooleanField(default=False)
    sidebar_right = models.BooleanField(default=False)
    primary_color = models.CharField(max_length=10)
    secondary_color = models.CharField(max_length=10)
    text_color = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = 'Interface'

    def __str__(self):
        return 'Interface'

class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Profile'

    def __str__(self):
        return self.username


class Email(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=50, null=True, blank=True)
    indication_color = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = 'Email'

    def __str__(self):
        return self.name

class ApiKey(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = 'Api Keys'

    def __str__(self):
        return self.name
