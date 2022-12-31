from django.forms import ModelForm
from .models import Interface, Profile, Email, Api, Theme


class ThemeForm(ModelForm):

    class Meta:
        model = Theme
        fields = '__all__'


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


class ApiForm(ModelForm):

    class Meta:
        model = Api
        fields = '__all__'
        exclude = ['user']
