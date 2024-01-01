# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm, ClientForm, PropertyForm, RentalPropertyForm, ClientSuggestionForm, ClientInterestForm
from Realtor.models import Property
from django.contrib import messages
from .models import Files, Event, Clent, Client_suggestion
from Realtor.models import PropertyImage
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.template.loader import render_to_string
import os
from django.http import HttpResponse
from django.views import View


def crm(request):
    # Create instances of the forms
    event_form = EventForm(prefix='event')
    client_form = ClientForm(prefix='client')

    # Pass the forms to the template
    return render(request, 'base_event.html', {'event_form': event_form, 'client_form': client_form})

def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            # Add any additional logic or redirect as needed
            return redirect('create_client')
    else:
        form = ClientForm()

    return render(request, 'create_client.html', {'form': form})

def add_property(request):
    if request.method == 'POST':
        property_form = PropertyForm(request.POST, request.FILES)
        property_images = request.FILES.getlist('property_image')

        if property_form.is_valid():
            property_instance = property_form.save(commit=False)
            property_instance.deal_type = 'selling'
            property_instance.price_month = 0
            property_instance.latitude = request.POST.get('latitude', '')
            property_instance.longitude = request.POST.get('longitude', '')
            property_instance.save()

            property_images_instances = [
                PropertyImage(property=property_instance, image=image)
                for image in property_images
            ]

            # Bulk create all PropertyImage instances
            PropertyImage.objects.bulk_create(property_images_instances)

            # Add success message or redirection logic
            messages.success(request, 'Property added successfully')
            return redirect('add_property')  # Adjust the URL to where you want to redirect after success
        else:
            messages.error(request, 'Form validation failed')

    else:
        property_form = PropertyForm()

    return render(request, 'add_property.html', {'property_form': property_form})

def add_rental_property(request):
    if request.method == 'POST':
        property_form = RentalPropertyForm(request.POST, request.FILES)
        property_images = request.FILES.getlist('property_image')
        if property_form.is_valid() :
            property_instance = property_form.save(commit=False)
            property_instance.deal_type = 'rental'
            property_instance.price_sqrm = 0
            property_instance.save()

            property_images_instances = [
                PropertyImage(property=property_instance, image=image)
                for image in property_images
            ]

            # Bulk create all PropertyImage instances
            PropertyImage.objects.bulk_create(property_images_instances)

            # Add success message or redirection logic
            messages.success(request, 'Property added successfully')
            return redirect('add_rental_property')  # Adjust the URL to where you want to redirect after success
        else:
            messages.error(request, 'Form validation failed')

    else:
        property_form = RentalPropertyForm()

    return render(request, 'add_rental_property.html', {'property_form': property_form})

def events_list(request):
    events = Event.objects.all()

    return render(request, 'events_list.html', {'events': events})

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            return redirect('add_event')
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})

def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Get the referrer URL from the POST data
    referrer = request.POST.get('referrer', '')

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()

            # Redirect to the referrer URL or a default URL
            return redirect(referrer)
    else:
        form = EventForm(instance=event)

    # Pass the referrer URL to the template
    return render(request, 'edit_event.html', {'form': form, 'event': event, 'referrer': referrer})

def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return JsonResponse({'message': 'Event deleted successfully'})
    return render(request, 'delete_event.html', {'event': event})

def events_by_property(request):
    # Assuming Event model has a ForeignKey named 'participant_property' that refers to Property model
    events = Event.objects.select_related('participant_property', 'participant_buyer', 'participant_owner').all()
    events_by_property = {}

    for event in events:
        property_id = event.participant_property.id
        if property_id not in events_by_property:
            events_by_property[property_id] = {
                'property': event.participant_property,
                'events': []
            }

        events_by_property[property_id]['events'].append(event)

    return render(request, 'events_by_property.html', {'events_by_property': events_by_property.values()})

from django.utils import timezone

def events_by_client(request):
    events = Event.objects.select_related('participant_buyer', 'participant_owner').all()

    today = timezone.now().date()

    events_by_client = []

    for event in events:
        client = event.participant_buyer

        # Check if the client is already in the list
        client_data = next((client_data for client_data in events_by_client if client_data['client'] == client), None)

        if client_data:
            # Append the event data to the existing client data
            client_data['events'].append({
                'event_type': event.event_type,
                'event_date': event.event_date,
                'client': client,
                'id': event.id,
                'property': event.participant_property.address,
            })
        else:
            # Create a new client data entry
            events_by_client.append({
                'client': client,
                'phone_number': client.phone_number,  # Add phone_number to the client data
                'events': [{
                    'event_type': event.event_type,
                    'event_date': event.event_date,
                    'client': client,
                    'id': event.id,
                    'property': event.participant_property.address,
                }],
            })

    return render(request, 'events_by_client.html', {'events_by_client': events_by_client})

def client_list(request):
    clients = Clent.objects.all()
    return render(request, 'client_list.html', {'clients': clients})



def client_events(request, client_id):
    client = get_object_or_404(Clent, id=client_id)
    events = Event.objects.filter(participant_buyer=client)

    # Retrieve all suggestions for the client
    suggestions = Client_suggestion.objects.filter(client=client_id)

    if request.method == 'POST':
        # Check if the form is for suggestion and process it
        if 'is_suggested' in request.POST:
            suggestion_id = request.POST.get('suggestion_id')
            suggestion = get_object_or_404(Client_suggestion, id=suggestion_id)
            form = ClientSuggestionForm(request.POST, instance=suggestion)

            if form.is_valid():
                form.save()
            else:
                pass
    else:
        form = ClientSuggestionForm()

    return render(request, 'client_events.html', {'client': client, 'events': events, 'form': form, 'suggestions': suggestions})

def properties_list(request):
    properties = Property.objects.all()
    locations = list(Property.objects.values('latitude','longitude','address','deal_type','property_type','total_rooms','id')[:100])
    return render(request, 'properties_list.html', {'properties': properties, 'locations':locations})

def property_events(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    events = Event.objects.filter(participant_property=property)
    suggestions = Client_suggestion.objects.filter(property=property_id)

    form = ClientSuggestionForm()
    editform = PropertyForm(instance=property)

    if request.method == 'POST':
        if 'is_suggested' in request.POST:
            # Process suggestion form submission
            suggestion_id = request.POST.get('suggestion_id')
            suggestion = get_object_or_404(Client_suggestion, id=suggestion_id)
            form = ClientSuggestionForm(request.POST, instance=suggestion)
            if form.is_valid():
                form.save()
            else:
                pass
        elif 'edit_property' in request.POST:
            # Process property edit form submission
            editform = PropertyForm(request.POST, instance=property)
            if editform.is_valid():
                editform.save()

    return render(request, 'property_events.html', {'property': property, 'events': events, 'form': form, 'suggestions': suggestions, 'editform': editform})

