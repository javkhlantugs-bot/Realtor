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

            # Authenticate the user using django-allauth's authentication backend
            user = authenticate(request, username=user_instance.username, password=request.POST.get('password1'), backend='allauth.account.auth_backends.AuthenticationBackend')
            if user is not None:
                login(request, user)
                return redirect('accounts:login') 
            else:
                # Handle authentication failure
                pass
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
