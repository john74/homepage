from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from accounts.models import CustomUser
from .models import Profile, Email, ApiKey, Theme, Interface
from .forms import ThemeForm, ProfileForm, InterfaceForm, EmailForm, ApiForm
# from .utils import create_email_services
from .utils import get_email_accounts
# from .utils import create_api_services
from .utils import group_form_data
from .utils import group_db_data
from .utils import get_changed_data
from .utils import save_form
from .utils import get_items_to_delete
from .utils import delete_items



@login_required()
def settings(request):
    user = CustomUser.objects.get(id=request.user.id)

    profiles = Profile.objects.filter(user=user.id)
    email_services = get_email_accounts(user)
    emails = Email.objects.filter(service__user=user)
    apis = ApiKey.objects.filter(user=user.id)
    interfaces = Interface.objects.filter(user=user.id)
    themes = Theme.objects.all()
    errors = {}

    if request.method == 'POST':
        data = request.POST
        prefixes = ['profile', 'email', 'api', 'interface', 'theme']
        db_data = {
            'profile': profiles, 'email': emails, 'api': apis,
            'interface': interfaces, 'theme': themes
        }
        models = {
            'profile': Profile, 'email': Email, 'api': ApiKey,
            'interface': Interface, 'theme': Theme
        }
        forms = {
            'profile': ProfileForm, 'email': EmailForm, 'api': ApiForm,
            'interface': InterfaceForm, 'theme': ThemeForm
        }

        for prefix in prefixes:
            grouped_form_data = group_form_data(data, prefix)
            grouped_db_data = group_db_data(db_data[prefix], grouped_form_data)
            changed_data = get_changed_data(grouped_form_data, grouped_db_data)
            if changed_data:
                model = models[prefix]
                form = forms[prefix]
                save_form(model, form, changed_data)

        items_to_delete = get_items_to_delete(data)
        if items_to_delete:
            delete_items(items_to_delete)
        return redirect('settings')

    context = {
        'profiles': profiles,
        'email_services': email_services,
        'apis': apis,
        'interfaces': interfaces,
        'themes': themes,
        'errors':errors
    }
    return render(request, 'settings.html', context)
