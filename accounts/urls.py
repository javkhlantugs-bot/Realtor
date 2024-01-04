# accounts/urls.py
from django.urls import path
from .views import register, user_login, user_logout, load_cities

app_name = 'accounts' 

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/load_cities/',load_cities, name='load_cities')
]
