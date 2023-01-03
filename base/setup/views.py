from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import CustomUserChangeForm
from settings.models import Profile, Interface, Theme, ApiKey, Email
from settings.forms import ProfileForm, InterfaceForm, EmailForm, ApiForm
from settings.utils import group_form_data
from settings.utils import group_db_data
from settings.utils import get_changed_data
from settings.utils import save_form
from .utils import create_email_services
from .utils import create_api_services
from .utils import create_profile
from .utils import create_interface
from .utils import add_search_engines
from .utils import create_themes
from .utils import create_api_keys
from .utils import create_emails

@login_required()
def setup(request):
    user = request.user
    if not user.first_login:
        return redirect('home:home')
    create_email_services(user)
    create_emails(user)
    create_api_services(user)
    create_api_keys(user)
    create_profile(user)
    create_themes(user)
    create_interface(user)
    add_search_engines()

    profile = Profile.objects.filter(id=user.id)
    interface = Interface.objects.filter(user=user.id)
    themes = Theme.objects.all()
    apis = ApiKey.objects.all()
    emails = Email.objects.filter(service__user=user)

    if request.method == 'POST':
        data = request.POST
        prefixes = ['profile', 'email', 'api', 'interface']
        db_data = {
            'profile': profile, 'email': emails, 'api': apis,
            'interface': interface
        }
        models = {
            'profile': Profile, 'email': Email, 'api': ApiKey,
            'interface': Interface
        }
        forms = {
            'profile': ProfileForm, 'email': EmailForm, 'api': ApiForm,
            'interface': InterfaceForm
        }

        for prefix in prefixes:
            grouped_form_data = group_form_data(data, prefix)
            grouped_db_data = group_db_data(db_data[prefix], grouped_form_data)
            changed_data = get_changed_data(grouped_form_data, grouped_db_data)
            if changed_data:
                model = models[prefix]
                form = forms[prefix]
                save_form(model, form, changed_data)
        form = CustomUserChangeForm({'email':user.email, 'first_login': False}, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home:home')

    context = {
        'profile': profile[0],
        'interface': interface[0],
        'themes': themes,
        'apis': apis,
        'emails': emails
    }
    return render(request, 'setup.html', context)
