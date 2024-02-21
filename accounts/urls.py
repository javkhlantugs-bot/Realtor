# accounts/urls.py
from django.urls import path
from .views import register, user_login, user_logout,privacy_policy,terms_of_service


app_name = 'accounts' 

urlpatterns = [
    path('', user_login, name='login'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('privacy_policy/', privacy_policy, name='privacy_policy'),
    path('terms_of_service/', terms_of_service, name='terms_of_service'),

    
]
