from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from accounts.models import CustomUser
from .models import Profile, Email
from .forms import ProfileForm
from .forms import InterfaceForm
from .forms import EmailForm
from .forms import ApiKeyForm
from .utils import create_email_services
from .utils import get_or_create_profile
from .utils import get_profile_form_data
from .utils import save_profile_form
from .utils import get_email_form_data
from .utils import get_email_accounts
from .utils import get_zipped_email_form_data
from .utils import get_zipped_email_db_data
from .utils import get_changed_email_data
from .utils import save_email_form


def settings(request):
    user_id = request.user.id
    user = CustomUser.objects.get(id=user_id)
    create_email_services(user)

    email_services = get_email_accounts(user)

    if request.method == 'POST':
        data = request.POST

        email_form_data = get_email_form_data(data)
        zipped_email_form_data = get_zipped_email_form_data(email_form_data)
        zipped_email_db_data = get_zipped_email_db_data(email_services)
        changed_email_data = get_changed_email_data(zipped_email_form_data, zipped_email_db_data)

        if changed_email_data:
            save_email_form(changed_email_data)

        return redirect('settings')

    context = {
        'email_services': email_services
    }
    return render(request, 'settings.html', context)
