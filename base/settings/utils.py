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


def group_test_data(data):
    grouped_data = []
    first_key = next(iter(data))
    loops = len(data[first_key])
    for index in range(loops):
        temp = {}
        for key, value in  data.items():
            temp[key] = value[index]
        grouped_data.append(temp)
    return grouped_data


def group_form_data(form_data, prefix):
    data = {}
    for field_name in form_data.keys():
        if field_name.startswith(prefix):
            values = form_data.getlist(field_name)
            db_field_name = field_name.replace(f'{prefix}-', '')
            data[db_field_name] = values
    # print('GROUPED FORM DATA -> ', group_test_data(data))
    return group_test_data(data)

def sanitize_object(value, form_data):
    form_fields = form_data[0].keys()
    fields_to_remove = []
    for field in value.keys():
        if field not in form_fields:
            fields_to_remove.append(field)
        if isinstance(value[field], int):
            value[field] = str(value[field])
    for field in fields_to_remove:
        del value[field]
    return value


def group_db_data(db_data, form_data):
    data = []
    for value in db_data.values():
        obj = sanitize_object(value, form_data)
        data.append(obj)
    # print('TEST DB DATA -> ', data)
    return data


def get_changed_data(form_data, db_data):
    changed_data = []
    for data in form_data:
        if data not in db_data:
            changed_data.append(data)
    return changed_data


def save_form(model, form, form_data):
    for data in form_data:
        try:
            instance = model.objects.get(id=data['id'])
        except model.DoesNotExist:
            instance = None

        model_form = form(data, instance=instance)
        if model_form.is_valid():
            new_form = model_form.save(commit=False)
            if model.__name__.lower() == 'email':
                try:
                    service = EmailService.objects.get(id=data['service_id'])
                except EmailService.DoesNotExist:
                    continue
                new_form.service = service
            new_form.save()
