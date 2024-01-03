from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create_client/', views.create_client, name='create_client'),
    path('events_list/', views.events_list, name='events_list'),
    path('add_property/', views.add_property, name='add_property'),
    path('add_rental_property/', views.add_rental_property, name='add_rental_property'),
    path('events/add/', views.add_event, name='add_event'),
    path('events/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('events/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('events/by_property/', views.events_by_property, name='events_by_property'),
    path('events/by_client/', views.events_by_client, name='events_by_client'),
    path('clients/', views.client_list, name='client_list'),
    path('clients/<int:client_id>/', views.client_events, name='client_events'),
    path('properties/', views.properties_list, name='properties_list'),
    path('properties/<int:property_id>/', views.property_events, name='property_events'),
]