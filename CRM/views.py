# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm, ClientForm, PropertyForm, RentalPropertyForm, ClientSuggestionForm, ClientWishForm, PropertyForm1, ClientForm1, ClientPhoneNumbers, ClientRelationships, PropertyImageForm
from Realtor.models import Property
from django.contrib import messages
from .models import Files, Event, Clent, Client_suggestion, ClientInterest
from Realtor.models import PropertyImage
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.template.loader import render_to_string
import os
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import requests


def dashboard(request):
    return render(request, 'crm_dashboard.html')

def crm(request):
    # Create instances of the forms
    event_form = EventForm(prefix='event')
    client_form = ClientForm(prefix='client')

    # Pass the forms to the template
    return render(request, 'base_event.html', {'event_form': event_form, 'client_form': client_form})

@login_required
def create_client(request):
    if request.method == 'POST':
        # Set the user field before saving the form
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.user = request.user  # Set the user field
            client.save()
            # Add any additional logic or redirect as needed
            return redirect('create_client')
    else:
        form = ClientForm()

    return render(request, 'create_client.html', {'form': form})

@login_required
def create_client_interest(request, client_id):
    client = get_object_or_404(Clent, id=client_id)

    if request.method == 'POST':
        form = ClientWishForm(user=request.user, data=request.POST)
        if form.is_valid():
            interest = form.save(commit=False)
            interest.client = client
            interest.save()
            return redirect('create_client_interest', client_id=client_id)
        else:
            print(form.errors)
    else:
        form = ClientWishForm(user=request.user)

    context = {
        'form': form,
        'client': client,
    }

    return render(request, 'create_client_interest.html', context)

@login_required
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
            property_instance.user = request.user
            property_instance.save()

            property_images_instances = [
                PropertyImage(property=property_instance, image=image)
                for image in property_images
            ]

            # Bulk create all PropertyImage instances
            PropertyImage.objects.bulk_create(property_images_instances)

            # Add success message or redirection logic
            messages.success(request, 'Property added successfully')
            property_id = property_instance.id
            property_edit_url = reverse('edit_property', args=[property_id])
            return redirect(property_edit_url)  # Adjust the URL to where you want to redirect after success
        else:
            messages.error(request, 'Form validation failed')

    else:
        property_form = PropertyForm()

    return render(request, 'add_property.html', {'property_form': property_form})

@login_required
def edit_property(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    photos = PropertyImage.objects.filter(property=property_id)
    # Get the referrer URL from the POST data
    referrer = request.POST.get('referrer', '')
    locations = list(Property.objects.values('latitude', 'longitude','id').filter(user=request.user.id, id = property_id))
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        property_images = request.FILES.getlist('property_image')
        if form.is_valid():
            property_instance = form.save(commit=False)
            property_instance.user = request.user
            property_instance.save()
            property_images_instances = [
                PropertyImage(property=property_instance, image=image)
                for image in property_images
            ]

            # Bulk create all PropertyImage instances
            PropertyImage.objects.bulk_create(property_images_instances)
            property_events_url = reverse('property_events', args=[property_id])
            # Redirect to the referrer URL or a default URL
            return redirect(property_events_url)
    else:
        form = PropertyForm(instance=property)

    # Pass the referrer URL to the template
    return render(request, 'edit_property.html', {'form': form, 'property': property, 'referrer': referrer,'locations': locations, 'photos':photos})

def delete_image(request, photo_id):
    try:
        photo = PropertyImage.objects.get(id=photo_id)
        photo.delete()
        return JsonResponse({'success': True})
    except PropertyImage.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Image does not exist'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
    
@login_required
def add_rental_property(request):
    if request.method == 'POST':
        property_form = RentalPropertyForm(request.POST, request.FILES)
        property_images = request.FILES.getlist('property_image')
        if property_form.is_valid() :
            property_instance = property_form.save(commit=False)
            property_instance.deal_type = 'rental'
            property_instance.price_sqrm = 0
            property_instance.user = request.user
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

from django.core.serializers import serialize

class EventsListView(View):
    template_name = 'events_list.html'

    def get(self, request, *args, **kwargs):
        events = Event.objects.filter(user=request.user.id)
        serialized_events = serialize('json', events)
        form = EventForm()

        context = {
            'events': serialized_events,
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        event_id = request.POST.get('event_id')  # Get event_id from the form if available
        form = EventForm(request.POST)
        
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user

            if event_id:  # Editing existing event
                existing_event = get_object_or_404(Event, pk=event_id, user=request.user)
                form = EventForm(request.POST, instance=existing_event)  # Use instance for editing
                if form.is_valid():
                    form.save()
                else :
                    print(form.errors)
            else:  # Creating new event
                event.save()

            return redirect('events_list')
        else:
            events = Event.objects.filter(user=request.user.id)
            serialized_events = serialize('json', events)
            return render(request, self.template_name, {'events': serialized_events, 'form': form})

@require_POST
def toggle_complete(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.is_completed = not event.is_completed
    event.save()
    return JsonResponse({'is_complete': event.is_completed})

class GetLocationsView(View):
    def get(self, request):
        selected_date = request.GET.get('selected_date')
        locations = list(
            Event.objects
            .values('participant_property__latitude', 'participant_property__longitude', 'id', 'event_hour','participant_property__address',
                    'event_minute', 'event_ampm','event_description')
            .filter(user=request.user.id, event_date=selected_date, is_completed = False)
        )
        return JsonResponse({'locations': locations})

class GetProperties(View):
    def get(self, request):
        property_id = request.GET.get('property_id')
        properties = list(
            Property.objects
            .values('id', 'address')
            .filter(user=request.user.id, id=property_id)
        )
        return JsonResponse({'properties': properties})

from django.db.models import Count
from django.db.models.functions import TruncDate

def get_events(request):
    events = (
        Event.objects
        .filter(user=request.user.id)
        .annotate(date=TruncDate('event_date'))
        .values('date')
        .annotate(event_count=Count('id'))
    )

    event_list = []
    for event in events:
        events_for_date = Event.objects.filter(user=request.user.id, event_date__date=event['date'])
        event_list.append({
            'date': event['date'].isoformat(),
            'count': event['event_count'],
            'events': [
                {
                    'title': e.event_type,
                    'start': e.event_date.isoformat(),
                    'end': e.event_date.isoformat(),
                } for e in events_for_date
            ]
        })

    print(event_list)  # Add this line to print the data
    return JsonResponse(event_list, safe=False)

@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('add_event')
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        event_form = EventForm(request.POST, instance=event)

        if event_form.is_valid():
            event_form.save()

            # Redirect to the referrer URL or a default URL
            return redirect('events_list')
        else:
            print(event_form.errors)
    else:
        event_form = EventForm(instance=event)

    return render(request, 'edit_event.html', {'form': event_form, 'event': event})
@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('events_list')
    
    return render(request, 'delete_event.html', {'event': event})

def client_list(request):
    clients = Clent.objects.filter(user=request.user.id)
    if request.method == 'POST':
        form = ClientForm1(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.user = request.user
            client.save()
            return redirect('client_list')
        else:
            print(form.errors)
    else:
        form = ClientForm1()
    return render(request, 'client_list.html', {'clients': clients,'form':form})

def client_events(request, client_id):
    client = get_object_or_404(Clent, id=client_id)
    events = Event.objects.filter(participant_buyer=client,user = request.user.id)
    wishes = ClientInterest.objects.filter(client = client, user = request.user.id)
    # Retrieve all suggestions for the client
    suggestions = Client_suggestion.objects.filter(client=client_id, user = request.user.id)
    interested_list = Client_suggestion.objects.filter(client=client_id, is_interested = 'interested', user = request.user.id)
    interested_map = list(
        interested_list.values('property__latitude', 'property__longitude', 'property__deal_type','property__property_type',
                               'property__total_rooms', 'property__address', 'property__id'))

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

    return render(request, 'client_events.html', {'client': client, 'events': events, 'form': form, 'suggestions': suggestions,'interested_map':interested_map, 'wishes':wishes})


@login_required
def edit_client(request, client_id):
    client = get_object_or_404(Clent, id=client_id)

    if request.method == 'POST':
        phone_numbers = ClientPhoneNumbers(request.POST)
        relationships = ClientRelationships(request.POST)
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            client_events_url = reverse('client_events', args=[client_id])
            # Redirect to the referrer URL or a default URL
            return redirect(client_events_url)
        else:
            print(form.errors)
        if phone_numbers.is_valid():
            phone_numbers.instance.user = request.user
            phone_numbers.save()
            client_events_url = reverse('client_events', args=[client_id])
            # Redirect to the referrer URL or a default URL
            return redirect(client_events_url)
        if relationships.is_valid():
            relationships.instance.user = request.user
            relationships.save()
            client_events_url = reverse('client_events', args=[client_id])
            # Redirect to the referrer URL or a default URL
            return redirect(client_events_url)

    else:
        form = ClientForm(instance=client)
        phone_numbers = ClientPhoneNumbers(instance=client)
        relationships = ClientRelationships(instance=client)

    # Pass the referrer URL to the template
    return render(request, 'edit_client.html', {'form': form, 'client': client,'phone_form':phone_numbers})

@login_required
def properties_list(request):
    properties = Property.objects.filter(user=request.user.id)
    locations = list(Property.objects.values('latitude', 'longitude', 'address', 'deal_type', 'property_type', 'total_rooms', 'id').filter(user=request.user.id))

    if request.method == 'POST':
        form = PropertyForm1(request.POST)
        if form.is_valid():
            property = form.save(commit=False)
            property.user = request.user
            property.save()
            return redirect('properties_list')
        else:
            print(form.errors)
    else:
        form = PropertyForm1()

    return render(request, 'properties_list.html', {'properties': properties, 'locations': locations, 'properties_form': form})

def property_events(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    events = Event.objects.filter(participant_property=property, user = request.user.id)
    suggestions = Client_suggestion.objects.filter(property=property_id)

    form = ClientSuggestionForm()

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

    return render(request, 'property_events.html', {'property': property, 'events': events, 'form': form, 'suggestions': suggestions})

from geopy.geocoders import Nominatim
def address_search(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        geolocator = Nominatim(user_agent="Estates.Solutions")

        try:
            locations = geolocator.geocode(query, exactly_one=False)
            results = [{'address': location.address, 'latitude': location.latitude, 'longitude': location.longitude} for location in locations]
            return JsonResponse({'results': results})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def search_page(request):
    return render(request, 'search.html')

def google_maps_proxy(request):
    api_key = 'AIzaSyAhi9zWHq375WASuDJ-sXrMWvDs9NK9lB4'
    url = f'https://maps.googleapis.com/maps/api/js?key={api_key}&callback=initAutocomplete&libraries=places&v=weekly'
    response = requests.get(url)
    
    return JsonResponse({'script': response.text})