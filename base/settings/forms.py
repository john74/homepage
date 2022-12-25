from django.forms import ModelForm
from .models import Interface, Profile, Email, ApiKey


class InterfaceForm(ModelForm):

    class Meta:
        model = Interface
        fields = '__all__'
        exclude = ['user']


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']


class EmailForm(ModelForm):

    class Meta:
        model = Email
        fields = '__all__'
        exclude = ['user', 'service']


class ApiKeyForm(ModelForm):

    class Meta:
        model = ApiKey
        fields = '__all__'
        exclude = ['user']
