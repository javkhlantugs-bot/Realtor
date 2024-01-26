from django.urls import path
from . import views

urlpatterns = [
    path('<str:client_link>/', views.ClientSuggestedPropertiesView.as_view(), name='client_suggested_properties'),
    path('show_properties/<str:user>/<int:id>/<str:address>/', views.show_property, name='show_property'),

]