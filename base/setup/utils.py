from django.db import IntegrityError
from settings.models import ApiKey, Profile, Interface, Theme, Email
from .models import SearchEngine, ApiService, EmailService
from .constants import SEARCH_ENGINES, EMAIL_SERVICES, APIS, DEFAULT_THEMES


def add_search_engines():
    for engine in SEARCH_ENGINES.values():
        try:
            SearchEngine.objects.create(
                name = engine['name'],
                url = engine['url'],
                form_action = engine['form_action'],
                form_method = engine['form_method'],
                name_attribute = engine['name_attribute'],
                default = engine['default']
            )
        except IntegrityError:
            continue


def create_themes(user):
    for theme in DEFAULT_THEMES.values():
        try:
            Theme.objects.create(
                user = user,
                name = theme['name'],
                primary_color = theme['primary_color'],
                secondary_color = theme['secondary_color'],
                text_color = theme['text_color']
            )
        except IntegrityError:
            continue


def create_email_services(user):
    for service in EMAIL_SERVICES:
        try:
            EmailService.objects.create(user=user, name=service)
        except IntegrityError:
            continue


def create_emails(user):
    services = EmailService.objects.filter(user=user)
    for service in services:
        try:
            Email.objects.get(service=service.id)
        except Email.DoesNotExist:
            Email.objects.create(service=service)


def create_api_services(user):
    for api in APIS:
        try:
            ApiService.objects.create(user=user, name=api)
        except IntegrityError:
            continue


def create_api_keys(user):
    services = ApiService.objects.filter(user=user)
    for service in services:
        try:
            ApiKey.objects.create(service=service)
        except IntegrityError:
            continue


def create_profile(user):
    try:
        Profile.objects.create(user=user)
    except IntegrityError:
        return


def create_interface(user):
    try:
        Interface.objects.create(user=user)
    except IntegrityError:
        return
