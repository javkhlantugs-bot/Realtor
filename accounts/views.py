# accounts/views.py
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from CRM.models import event_type_model, client_status_types

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user_instance = form.save(commit=False)
            user_instance.region = request.POST.get('region')
            user_instance.save()

            # Create EventType records
            event_type_model.objects.create(user=user_instance, event_type="Meeting")
            event_type_model.objects.create(user=user_instance, event_type="Show property")

            # Create ClientStatusTypes records
            client_status_types.objects.create(user=user_instance, status="Active")
            client_status_types.objects.create(user=user_instance, status="Inactive")

            login(request, user_instance)
            return redirect('accounts:login') 
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
            return redirect(success_url) 
        else:
            print(form.errors)
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('accounts:login')
