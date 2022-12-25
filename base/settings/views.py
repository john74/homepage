from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from accounts.models import CustomUser
from .models import Profile, Email
from .forms import ProfileForm
from .forms import InterfaceForm
from .forms import EmailForm
from .forms import ApiKeyForm
from .utils import get_or_create_email_services
from .utils import get_or_create_profile
from .utils import get_profile_form_data
from .utils import save_profile_form
from .utils import get_email_form_data


def settings(request):
    user = CustomUser.objects.get(email=request.user.email)
    emails = get_or_create_email_services(user)
    profile = get_or_create_profile(user)

    if request.method == 'POST':
        data = request.POST

        profile_form_data = get_profile_form_data(data, profile)
        if profile_form_data:
            save_profile_form(profile_form_data)

        email_form_data = get_email_form_data(data, emails)

        return redirect('settings')

    context = {
        'profile': profile,
        'emails': emails
    }
    return render(request, 'settings.html', context)
