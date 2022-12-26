from .models import Profile
from .models import ApiKey
from .models import EmailService
from .models import Email
from .forms import ProfileForm
from .forms import EmailForm
from .forms import ApiKeyForm


def create_api_services(user):
    services = ApiKey.objects.filter(user=user.id)
    if services:
        return services
    services = ['Open Weather']
    for service in services:
        ApiKey.objects.create(user=user, name=service)


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
        form_field_values = form_data.getlist(f'email-{field_name}')
        email_form_data[field_name] = form_field_values
    return email_form_data


def get_zipped_email_form_data(form_data):
    return zip(
        form_data['id'],
        form_data['service'],
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
                str(account.service.id),
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

        try:
            email_instance = Email.objects.get(id=email_id)
        except Email.DoesNotExist:
            email_instance = None

        form = EmailForm(
            {
                'email': data[2],
                'password': data[3],
                'category': data[4],
                'color': data[5]
            },
            instance=email_instance
        )

        service_id = data[1]
        try:
            service = EmailService.objects.get(id=service_id)
        except EmailService.DoesNotExist:
            return

        if form.is_valid():
            email_form = form.save(commit=False)
            email_form.service = service
            email_form.save()


def get_or_create_profile(user):
    try:
        return Profile.objects.get(user=user.id)
    except Profile.DoesNotExist:
        return Profile.objects.create(user=user)


def get_form_data(model, form_data):
    model_field_names = [field.name for field in model._meta.get_fields()]
    model_form_data = {}
    field_prefix = model._meta.verbose_name.lower()
    for field_name in model_field_names:
        if field_name in ['user']:
            continue
        form_field_values = form_data.getlist(f'{field_prefix}-{field_name}')
        model_form_data[field_name] = form_field_values[0]
    return model_form_data


def get_profile_db_data(profile):
    return {
        'id': str(profile.id),
        'username': profile.username,
        'country': profile.country,
        'city': profile.city
    }


def get_changed_profile_data(form_data, db_data):
    if form_data != db_data:
        return form_data
    return


def save_profile_form(data):
    profile_id = data['id']
    try:
        profile = Profile.objects.get(id=profile_id)
    except Profile.DoesNotExist:
        return
    form = ProfileForm(data, instance=profile)
    if form.is_valid():
        profile_form = form.save(commit=False)
        profile_form.user = profile.user
        profile_form.save()
    return


def group_data(data):
    d = []
    first_key = next(iter(data))
    max_loops = len(data[first_key])
    for loop in range(max_loops):
        temp = {}
        for key, value in data.items():
            temp[key] = value[loop]
        d.append(temp)
    return d


def get_api_form_data(model, form_data):
    model_field_names = [field.name for field in model._meta.get_fields()]
    model_form_data = {}
    field_prefix = model._meta.verbose_name.lower()
    for field_name in model_field_names:
        form_field_values = form_data.getlist(f'{field_prefix}-{field_name}')
        if form_field_values:
            model_form_data[field_name] = form_field_values
    return group_data(model_form_data)


def get_zipped_api_db_data(form_data):
    data = []
    for value in form_data.values():
        del value['user_id']
        value['id'] = str(value['id'])
        data.append(value)
    return data


def get_changed_api_data(form_data, db_data):
    changed_data = []
    for data in form_data:
        if data not in db_data:
            changed_data.append(data)
    return changed_data

def save_api_form(api_data):
    for data in api_data:
        try:
            instance = ApiKey.objects.get(id=data['id'])
        except ApiKey.DoesNotExist:
            continue
        form = ApiKeyForm(data, instance=instance)
        if form.is_valid():
            form.save()
