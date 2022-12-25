from .models import Profile
from .models import Email
from .forms import ProfileForm
from .forms import EmailForm


def get_or_create_email_services(user):
    services = Email.objects.filter(user=user.id)
    if services:
        return services
    services = ['Gmail', 'Proton Mail']
    for service in services:
        Email.objects.create(user=user, service=service)


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


def get_email_form_data(data, emails):
    print('DATA -> ', data)
    print('=============================')
    for email in emails.values():
        print('DATABASE EMAIL -> ', email)
        # print('DATA DICT -> ', data)
        # print('=============================')
        # print('EMAIL DICT -> ', email)
        # print('=============================')
        # print('TUPLE -> ', tuple(email.values()))
