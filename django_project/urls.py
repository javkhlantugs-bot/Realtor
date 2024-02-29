"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf.urls.static import static
from django.conf import settings
from accounts.views import user_login
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('crm/',include('CRM.urls')),
    path('card/', include('suggest_properties.urls')),
    path('', include('accounts.urls', namespace='accounts')),
    path('', include('allauth.urls')),
    path('', include('django.contrib.auth.urls')),
    path('login/', user_login, name='user_login'),
    
    path('reset_password/', 
        auth_views.PasswordResetView.as_view(
             template_name = 'reset_password.html'), 
            name='reset_password'),
    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name = 'reset_password_sent.html'), 
            name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name = 'reset.html'), 
            name='password_reset_confirm'),
    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name = 'password_reset_complete.html'), 
            name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
