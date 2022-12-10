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
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
        return redirect('login_user')

    form = CustomUserCreationForm()
    context = {'form':form}
    return render(request, 'register.html', context)
