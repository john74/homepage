from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    '''
    Overrides Django's default UserManager.
    '''
    use_in_migrations: True

    def _create_user(self, email, password=None, **extra_fields):
        '''
        Saves a user to the database, wether it is a simple user
        or a super user.
        '''
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user



    def create_user(self, email, password=None, **extra_fields):
        '''
        Overrides Django's default create_user method of the User model.
        '''
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        '''
        Overrides Django's default create_superuser method of the User model.
        '''
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    '''
    CustomUser model that substitues Django's built-in
    User model. It uses the email as the identification
    token instead of the username.AUTH_USER_MODEL in settings.py
    must point to the CustomUser model.
    https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
    '''
    username = None
    email = models.EmailField(unique=True)
    first_login = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email
