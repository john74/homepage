from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from accounts.models import CustomUser
from .models import Profile, Email, ApiKey
from .forms import ProfileForm
from .forms import InterfaceForm
from .forms import EmailForm
from .forms import ApiKeyForm
from .utils import create_email_services
from .utils import get_or_create_profile
from .utils import save_profile_form
from .utils import get_email_form_data
from .utils import get_email_accounts
from .utils import get_zipped_email_form_data
from .utils import get_zipped_email_db_data
from .utils import get_changed_email_data
from .utils import save_email_form
from .utils import get_form_data
from .utils import get_profile_db_data
from .utils import get_changed_profile_data
from .utils import create_api_services
from .utils import get_api_form_data
from .utils import get_zipped_api_db_data
from .utils import get_changed_api_data
from .utils import save_api_form


def settings(request):
    user_id = request.user.id
    user = CustomUser.objects.get(id=user_id)
    create_email_services(user)
    create_api_services(user)

    profile = Profile.objects.get(user=user_id)
    email_services = get_email_accounts(user)
    apis = ApiKey.objects.filter(user=user.id)

    if request.method == 'POST':
        data = request.POST

        profile_form_data = get_form_data(Profile, data)
        profile_db_data = get_profile_db_data(profile)
        changed_profile_data = get_changed_profile_data(profile_form_data, profile_db_data)
        if changed_profile_data:
            save_profile_form(changed_profile_data)

        email_form_data = get_email_form_data(data)
        zipped_email_form_data = get_zipped_email_form_data(email_form_data)
        zipped_email_db_data = get_zipped_email_db_data(email_services)
        changed_email_data = get_changed_email_data(zipped_email_form_data, zipped_email_db_data)

        if changed_email_data:
            save_email_form(changed_email_data)

        api_form_data = get_api_form_data(ApiKey, data)
        api_db_data = get_zipped_api_db_data(apis)
        changed_api_data = get_changed_api_data(api_form_data, api_db_data)
        if changed_api_data:
            save_api_form(changed_api_data)



        return redirect('settings')

    context = {
        'profile': profile,
        'email_services': email_services,
        'apis': apis
    }
    return render(request, 'settings.html', context)
