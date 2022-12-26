from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from accounts.models import CustomUser
from .models import Profile
from .models import Email
from .models import ApiKey
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


def settings(request):
    user_id = request.user.id
    user = CustomUser.objects.get(id=user_id)
    create_email_services(user)
    create_api_services(user)

    profiles = Profile.objects.filter(user=user_id)
    email_services = get_email_accounts(user)
    apis = ApiKey.objects.filter(user=user.id)

    if request.method == 'POST':
        data = request.POST
        # print('POST DATA -> ', data)

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



        return redirect('settings')

    context = {
        'profiles': profiles,
        'email_services': email_services,
        'apis': apis
    }
    return render(request, 'settings.html', context)
