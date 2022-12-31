from .models import Profile
from .models import ApiKey
from .models import EmailService
from .models import Email
from .forms import ProfileForm
from .forms import EmailForm
from .forms import ApiKeyForm
from .models import Theme


def get_items_to_delete(data):
    items_to_delete = []
    for item in data:
        if 'delete' in item:
            items_to_delete.append(item)
    return items_to_delete


def delete_items(items):
    models = {'theme': Theme, 'email': Email}
    for item in items:
        try:
            # delete-theme-10
            model = models[item.split('-')[1]] # Theme
            item_id = item.split('-')[-1] # 10
            obj = model.objects.get(id=item_id)
        except (IndexError, KeyError, Theme.DoesNotExist, Email.DoesNotExist):
            return
        obj.delete()


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
        if prefix in field_name and 'delete' not in field_name:
            values = form_data.getlist(field_name)
            db_field_name = field_name.replace(f'{prefix}-', '')
            data[db_field_name] = values
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
        # print('DATA INSIDE SAVE FORM -> ', data)
        try:
            instance = model.objects.get(id=data['id'])
        except model.DoesNotExist:
            instance = None
        # print('INSTANCE INSIDE SAVE FORM -> ', instance)
        model_form = form(data, instance=instance)
        # print('MODEL FORM INSIDE SAVE FORM -> ', model_form)
        # print('MODEL FORM ERRORS -> ', model_form.errors.as_data())
        errors = model_form.errors
        if errors:
            # print('ERRORS AAAAA -> ', errors)
            return errors
        if model_form.is_valid():
            # print('MODEL NAME -> ', model.__name__.lower())
            new_form = model_form.save(commit=False)
            if model.__name__.lower() == 'email':
                try:
                    service = EmailService.objects.get(id=data['service_id'])
                except EmailService.DoesNotExist:
                    continue
                new_form.service = service
            new_form.save()
