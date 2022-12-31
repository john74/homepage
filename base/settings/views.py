from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from accounts.models import CustomUser
from .models import Profile
from .models import Email
from .models import ApiKey
from .models import Theme
from .models import Interface
from .forms import ThemeForm
from .forms import ProfileForm
from .forms import InterfaceForm
from .forms import EmailForm
from .forms import ApiKeyForm
from .utils import create_email_services
from .utils import get_email_accounts
from .utils import create_api_services
from .utils import group_form_data
from .utils import group_db_data
from .utils import get_changed_data
from .utils import save_form
from .utils import get_items_to_delete
from .utils import delete_items


def settings(request):
    user = CustomUser.objects.get(id=request.user.id)
    create_email_services(user)
    create_api_services(user)

    profiles = Profile.objects.filter(user=user.id)
    email_services = get_email_accounts(user)
    apis = ApiKey.objects.filter(user=user.id)
    interface_settings = Interface.objects.filter(user=user.id)
    themes = Theme.objects.all()
    errors = {}

    if request.method == 'POST':
        data = request.POST

        grouped_profile_form_data = group_form_data(data, 'profile')
        grouped_profile_db_data = group_db_data(profiles, grouped_profile_form_data)
        changed_profile_data = get_changed_data(grouped_profile_form_data, grouped_profile_db_data)
        if changed_profile_data:
            save_form(Profile, ProfileForm, changed_profile_data)

        emails = Email.objects.filter(service__user=user)
        grouped_email_form_data = group_form_data(data, 'email')
        grouped_email_db_data = group_db_data(emails, grouped_email_form_data)
        changed_email_data = get_changed_data(grouped_email_form_data, grouped_email_db_data)
        if changed_email_data:
            save_form(Email, EmailForm, changed_email_data)

        grouped_api_form_data = group_form_data(data, 'api')
        grouped_api_db_data = group_db_data(apis, grouped_api_form_data)
        changed_api_data = get_changed_data(grouped_api_form_data, grouped_api_db_data)
        if changed_api_data:
            save_form(ApiKey, ApiKeyForm, changed_api_data)

        grouped_int_form_data = group_form_data(data, 'interface')
        # print('GROUPED INT FORM DATA -> ', grouped_int_form_data)
        grouped_int_db_data = group_db_data(interface_settings, grouped_int_form_data)
        # print('GROUPED INT DB DATA -> ', grouped_int_db_data)
        changed_int_data = get_changed_data(grouped_int_form_data, grouped_int_db_data)
        if changed_int_data:
            save_form(Interface, InterfaceForm, changed_int_data)

        grouped_theme_form_data = group_form_data(data, 'theme')
        grouped_theme_db_data = group_db_data(themes, grouped_theme_form_data)
        changed_theme_data = get_changed_data(grouped_theme_form_data, grouped_theme_db_data)
        # print('GROUPED THEME FORM DATA -> ', grouped_theme_form_data)
        if changed_theme_data:
            errors = save_form(Theme, ThemeForm, changed_theme_data)

        items_to_delete = get_items_to_delete(data)
        if items_to_delete:
            delete_items(items_to_delete)
        return redirect('settings')

    context = {
        'profiles': profiles,
        'email_services': email_services,
        'apis': apis,
        'interface_settings': interface_settings,
        'themes': themes,
        'errors':errors
    }
    return render(request, 'settings.html', context)
