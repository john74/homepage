from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import CustomUser
from .forms import CustomUserCreationForm


def home(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    return render(request, 'home.html')


def login_user(request):
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
    return render(request, 'login.html')


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
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            passwords_match = password1 == password2
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
            'name':'email',
            'id':'email',
            'label':'email'
        },
        'Password': {
            'type':'password',
            'name':'password1',
            'id':'password1',
            'label':'password1'
        },
        'Repeat password': {
            'type':'password',
            'name':'password2',
            'id':'password2',
            'label':'password2'
        },
    }
    context = {'fields':fields}
    return render(request, 'register.html', context)
