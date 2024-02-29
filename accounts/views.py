# accounts/views.py
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, HttpResponse
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from CRM.models import event_type_model, client_status_types
from Realtor.models import property_status, property_type
from django.core.mail import send_mail


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['accept_policies']:
                user_instance = form.save(commit=False)
                user_instance.region = request.POST.get('region')
                user_instance.save()

                # Authenticate the user using django-allauth's authentication backend
                user = authenticate(request, username=user_instance.username, password=request.POST.get('password1'), backend='allauth.account.auth_backends.AuthenticationBackend')
                if user is not None:
                    login(request, user)
                    return redirect('accounts:login') 
                else:
                    # Handle authentication failure
                    pass
            else:
                # Handle case where policies are not accepted
                return HttpResponse("You must accept the Privacy Policy and Terms of Service.")
        else: 
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

import django.utils.timezone
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

def privacy_policy(request):
    return render(request,'privacy_policy.html')

def terms_of_service(request):

    return render(request,'terms_of_service.html')

