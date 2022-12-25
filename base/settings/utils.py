from .models import Profile
from .models import EmailService
from .models import Email
from .forms import ProfileForm
from .forms import EmailForm


def create_email_services(user):
    services = EmailService.objects.filter(user=user.id)
    if services:
        return services
    services = ['Gmail', 'Proton Mail']
    for service in services:
        EmailService.objects.create(user=user, service=service)


def get_email_accounts(user):
    services = EmailService.objects.filter(user=user.id)
    accounts = {}
    for service in services:
        accounts[service] = Email.objects.filter(service=service)
    return accounts


def get_email_form_data(form_data):
    email_model_field_names = [field.name for field in Email._meta.get_fields()]
    email_form_data = {}
    for field_name in email_model_field_names:
        if field_name in ['service']:
            continue
        form_field_values = form_data.getlist(f'email-{field_name}')
        email_form_data[field_name] = form_field_values
    return email_form_data


def get_zipped_email_form_data(form_data):
    return zip(
        form_data['id'],
        form_data['email'],
        form_data['password'],
        form_data['category'],
        form_data['color']
    )


def get_zipped_email_db_data(services):
    data = []
    for accounts in services.values():
        for account in accounts:
            data.append(tuple([
                str(account.id),
                account.email,
                account.password,
                account.category,
                account.color
            ]))
    return data


def get_changed_email_data(form_data, db_data):
    changed_data = []
    for data in form_data:
        if data not in db_data:
            changed_data.append(data)
    return changed_data


def save_email_form(email_data):
    for data in email_data:
        email_id = data[0]
        email_instance = Email.objects.get(id=email_id)
        form = EmailForm(
            {
                'email': data[1],
                'password': data[2],
                'category': data[3],
                'color': data[4]
            },
            instance=email_instance
        )
        if form.is_valid():
            service = EmailService.objects.get(id=email_instance.service.id)
            email_form = form.save(commit=False)
            email_form.service = service
            email_form.save()

def get_or_create_profile(user):
    try:
        return Profile.objects.get(user=user.id)
    except Profile.DoesNotExist:
        return Profile.objects.create(user=user)


def get_profile_form_data(data, profile):
    # exclude id and user fields
    profile_field_names = [field.name for field in profile._meta.get_fields()[2:]]
    changed_data = {}
    for field_name in profile_field_names:
        field_value = getattr(profile, field_name)
        if field_value is None:
            field_value = ''
        form_field_value = data.get(field_name)
        if field_value != form_field_value:
            changed_data[field_name] = form_field_value
    if changed_data:
        changed_data['id'] = profile.id
    return changed_data


def save_profile_form(data):
    profile_id = data['id']
    profile = Profile.objects.get(id=profile_id)
    form = ProfileForm(data, instance=profile)
    if form.is_valid():
        profile_form = form.save(commit=False)
        profile_form.user = profile.user
        profile_form.save()
    return
