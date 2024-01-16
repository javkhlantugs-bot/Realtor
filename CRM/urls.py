from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create_client/', views.create_client, name='create_client'),
    path('events_list/', views.EventsListView.as_view(), name='events_list'),
    path('get_locations/', views.GetLocationsView.as_view(), name='get_locations'),
    path('get_properties/', views.GetProperties.as_view(), name='get_properties'),
    path('get_events/', views.get_events, name='get_events'),
    path('add_property/', views.add_property, name='add_property'),
    path('add_rental_property/', views.add_rental_property, name='add_rental_property'),
    path('events/add/', views.add_event, name='add_event'),
    path('events/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('events/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('events/toggle_complete/<int:event_id>/', views.toggle_complete, name='toggle_complete'),
    path('clients/', views.client_list, name='client_list'),
    path('clients/<int:client_id>/', views.client_events, name='client_events'),
    path('clients/edit/<int:client_id>/', views.edit_client, name='edit_client'),
    path('properties/', views.properties_list, name='properties_list'),
    path('properties/<int:property_id>/', views.property_events, name='property_events'),
    path('properties/edit/<int:property_id>/', views.edit_property, name='edit_property'),
    path('create_client_interest/<int:client_id>/', views.create_client_interest, name='create_client_interest'),
    path('search/', views.search_page, name='search_page'),
    path('google-maps-script/', views.google_maps_proxy, name='google_maps_proxy'),
    path('delete_image/<int:photo_id>/', views.delete_image, name='delete_image'),
]