from django.urls import path
from . import views



urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create_client/', views.create_client, name='create_client'),
    path('events_list/', views.EventsListView.as_view(), name='events_list'),
    path('get_locations/', views.GetLocationsView.as_view(), name='get_locations'),
    path('get_properties/', views.GetProperties.as_view(), name='get_properties'),
    path('get_event_types/', views.GetEventTypes.as_view(), name='get_event_types'),
    path('get_clients/', views.GetClients.as_view(), name='get_clients'),
    path('get_events/', views.get_events, name='get_events'),
    path('add_property/', views.add_property, name='add_property'),
    path('add_rental_property/', views.add_rental_property, name='add_rental_property'),
    path('events/add/', views.add_event, name='add_event'),
    path('events/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('events/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('events/toggle_complete/<int:event_id>/', views.toggle_complete, name='toggle_complete'),
    path('events/add_event_type/', views.add_event_type, name='add_event_type'),
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
    path('settings/',views.settings, name='settings'),
    path('settings/google-authenticate/', views.google_authenticate, name='google_authenticate'),
    path('settings/import-google-contacts/', views.import_google_contacts, name='import_google_contacts'),
    path('settings/event_types_list/', views.event_types_list, name='event_types_list'),
    path('settings/edit_event_type/<int:event_type_id>/', views.edit_event_type, name='edit_event_type'),
    path('settings/delete_event_type/<int:event_type_id>/', views.delete_event_type, name='delete_event_type'),
]