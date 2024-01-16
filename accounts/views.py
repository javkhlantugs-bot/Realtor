# accounts/views.py
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.urls import reverse_lazy

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user_instance = form.save(commit=False)
            print(request.POST.get('region'))
            user_instance.region = request.POST.get('region')
            user_instance.save()
            login(request, user_instance)
            return redirect('accounts:login')  # Redirect to the home page
        else: 
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            success_url = reverse_lazy('dashboard')
            return redirect(success_url)  # Redirect to the home page
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('accounts:login')
