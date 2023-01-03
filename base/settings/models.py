from django.db import models
from accounts.models import CustomUser
from setup.models import EmailService, ApiService


class Theme(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    primary_color = models.CharField(max_length=9, null=True, blank=True, default='')
    secondary_color = models.CharField(max_length=9, null=True, blank=True, default='')
    text_color = models.CharField(max_length=9, null=True, blank=True, default='')

    class Meta:
        verbose_name = 'Theme'
        verbose_name_plural = 'Themes'

    def __str__(self):
        return self.name


class Interface(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, default=1)
    dark_mode = models.BooleanField(default=True)
    sidebar_right = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Interface'
        verbose_name_plural = 'Interface'

    def __str__(self):
        return 'Interface'


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, null=True, blank=True, default='')
    country = models.CharField(max_length=100, null=True, blank=True, default='')
    city = models.CharField(max_length=100, null=True, blank=True, default='')

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profile'

    def __str__(self):
        return 'Profile'


class Email(models.Model):
    service = models.ForeignKey(EmailService, on_delete=models.CASCADE)
    email = models.EmailField(unique=True, max_length=100, null=True, blank=True)
    password = models.CharField(max_length=50, null=True, blank=True, default='')
    category = models.CharField(max_length=10, null=True, blank=True, default='')
    color = models.CharField(max_length=10, null=True, blank=True, default='')

    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'

    def __str__(self):
        return self.email if self.email else self.service.name


class ApiKey(models.Model):
    service = models.OneToOneField(ApiService, on_delete=models.CASCADE)
    key = models.CharField(max_length=500, null=True, blank=True, default='')

    class Meta:
        verbose_name = 'Api Key'
        verbose_name_plural = 'Api Keys'

    def __str__(self):
        return 'Api Key'
