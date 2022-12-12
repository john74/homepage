from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import CustomUser
from .forms import CustomUserCreationForm


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return redirect('login_user')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    fields = {
        'Email': {
            'type':'email',
            'id':'email',
            'placeholder':'Enter your email'
        },
        'Password': {
            'type':'password',
            'id':'password',
            'placeholder':'Enter password'
        }
    }
    context = {'fields':fields}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login_user')


def register_user(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            CustomUser.objects.get(email=email)
            messages.info(request, 'User already exists.')
        except CustomUser.DoesNotExist:
            passwords_match = request.POST.get('password1') == request.POST.get('password2')
            if passwords_match:
                form = CustomUserCreationForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.info(request, 'User created successfully')
            else:
                messages.info(request, 'Passwords do not match.')
                return redirect('register_user')
        return redirect('login_user')

    form = CustomUserCreationForm()
    fields = {
        'Email': {
            'type':'email',
            'id':'email',
            'placeholder':'Enter your email'
        },
        'Country': {
            'type':'text',
            'id':'country',
            'placeholder':'Enter your country'
        },
        'City': {
            'type':'text',
            'id':'city',
            'placeholder':'Enter your city'
        },
        'Password': {
            'type':'password',
            'id':'password1',
            'placeholder':'Enter password'
        },
        'Repeat password': {
            'type':'password',
            'id':'password2',
            'placeholder':'Repeat password'
        },
    }
    context = {'fields':fields}
    return render(request, 'register.html', context)
