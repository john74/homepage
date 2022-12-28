from django.db import models
from accounts.models import CustomUser


class Theme(models.Model):
    name = models.CharField(max_length=10, unique=True)
    primary_color = models.CharField(max_length=10)
    secondary_color = models.CharField(max_length=10)
    text_color = models.CharField(max_length=10)

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


class EmailService(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="+")
    name = models.CharField(max_length=40, unique=True)

    class Meta:
        verbose_name_plural = 'Email Services'

    def __str__(self):
        return self.name


class Email(models.Model):
    service = models.ForeignKey(EmailService, on_delete=models.CASCADE)
    email = models.EmailField(unique=True, max_length=100, null=True, blank=True, default='')
    password = models.CharField(max_length=50, null=True, blank=True, default='')
    category = models.CharField(max_length=10, null=True, blank=True, default='')
    color = models.CharField(max_length=10, null=True, blank=True, default='')

    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'

    def __str__(self):
        return self.email


class ApiKey(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True, default='')
    key = models.CharField(max_length=500, null=True, blank=True, default='')

    class Meta:
        verbose_name = 'Api'
        verbose_name_plural = 'Api Keys'

    def __str__(self):
        return self.name
