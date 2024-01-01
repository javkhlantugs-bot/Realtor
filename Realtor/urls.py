from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('client_resources/', views.client_resources, name='client_resources'),
    path('properties/', views.properties, name='properties'),
    path('buy_properties/', views.buy_properties, name='buy_properties'),
    path('buy_properties/<int:id>/',views.detail_view, name='detail'),
    path('rent_properties/', views.rent_properties, name='rent_properties'),
    path('rent_properties/<int:id>/',views.detail_view_rental, name='detail_view_rental'),
    path('to_rent_properties/', views.to_rent_properties, name='to_rent_properties'),
    path('sell_properties/', views.sell_properties, name='sell_properties'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)