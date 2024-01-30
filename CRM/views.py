# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm, ClientForm, PropertyForm, RentalPropertyForm, ClientSuggestionForm, PropertyForm1, ClientForm1, ClientPhoneNumbers, ClientRelationships, PropertyImageForm, EventTypeForm, ClientInterestForm, suggestion_link_setup
from Realtor.models import Property
from django.contrib import messages
from .models import Files, Event, Clent, Client_suggestion, ClientInterest, event_type_model, suggestion_link_settings
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
        events = Event.objects.filter(user=request.user.id).select_related('event_type')
        eventtypes = event_type_model.objects.filter(user = request.user.id)
        # Create a mapping of event_type IDs to their names
        eventtype_map = {str(et.pk): et.event_type for et in eventtypes}

        serialized_events = serialize('json', events, use_natural_primary_keys=True, use_natural_foreign_keys=True)

        form = EventForm(user = request.user.id)

        context = {
            'events': serialized_events,
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        event_id = request.POST.get('event_id')  # Get event_id from the form if available
        form = EventForm(request.POST, user = request.user.id)
        
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user

            if event_id:  # Editing existing event
                existing_event = get_object_or_404(Event, pk=event_id, user=request.user)
                form = EventForm(request.POST, instance=existing_event, user = request.user.id)  # Use instance for editing
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

class GetClients(View):
    def get(self, request):
        client_id = request.GET.get('client_id')
        clients = list(
            Clent.objects
            .values('id', 'client_name')
            .filter(user=request.user.id, id=client_id)
        )
        return JsonResponse({'clients': clients})

class GetEventTypes(View):
    def get(self, request):
        event_type_id = request.GET.get('event_type_id')
        event_types = list(
            event_type_model.objects
            .values('id', 'event_type')
            .filter(user=request.user.id, id=event_type_id)
        )
        print(event_types)
        return JsonResponse({'event_types': event_types})

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
        form = EventForm(request.POST,user = request.user.id)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('add_event')
        else:
            print(form.errors)
    else:
        form = EventForm(user = request.user.id)
    return render(request, 'add_event.html', {'form': form})

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        event_form = EventForm(request.POST, instance=event, user = request.user.id)

        if event_form.is_valid():
            event_form.save()

            # Redirect to the referrer URL or a default URL
            return redirect('events_list')
        else:
            print(event_form.errors)
    else:
        event_form = EventForm(instance=event, user = request.user.id)

    return render(request, 'edit_event.html', {'form': event_form, 'event': event})

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('events_list')
    
    return render(request, 'delete_event.html', {'event': event})

@login_required
def delete_property(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        property.delete()
        return redirect('properties_list')
    
    return render(request, 'delete_property.html', {'property': property})

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
    suggested_list = Client_suggestion.objects.filter(client=client_id, is_suggested = 'suggested', is_interested='not_interested', user = request.user.id)
    rest_list = Client_suggestion.objects.filter(client=client_id, is_suggested = 'not_suggested',is_interested='not_interested', user = request.user.id)
    
    rest_map = list(
        rest_list.values('property__latitude', 'property__longitude', 'property__deal_type','property__property_type',
                               'property__total_rooms', 'property__address', 'property__id'))
    suggested_map = list(
        suggested_list.values('property__latitude', 'property__longitude', 'property__deal_type','property__property_type',
                               'property__total_rooms', 'property__address', 'property__id'))
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

    return render(request, 'client_events.html', {'client': client, 'events': events, 'form': form, 'suggestions': suggestions,'interested_map':interested_map, 'wishes':wishes,'suggested_map':suggested_map,'rest_map':rest_map})

def add_client_notes(request, client_id):
    if request.method == 'POST':
        form = ClientInterestForm(request.POST)
        client = get_object_or_404(Clent, id=client_id)
        if form.is_valid():
            interest = form.save(commit=False)
            interest.user = request.user
            interest.client = client
            interest.save()
            return redirect('client_events', client_id=client_id)
        else:
            print(form.errors)
    else:
        form = ClientInterestForm()
    return render(request, 'add_client_notes.html', {'form': form,'client_id':client_id})

def delete_client_note(request, note_id, client_id):
    note = get_object_or_404(ClientInterest, id=note_id)
    if request.method == 'POST':
        note.delete()
        return JsonResponse({'message': 'Note deleted successfully'})

    
    return render(request, 'delete_client_note.html', {'note': note})

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


from django.shortcuts import render, redirect
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path
import json
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']

# def google_authenticate(request):
#     # Get the path to the current directory
#     current_directory = Path(__file__).resolve().parent
#     # Path to the client secret file
#     client_secret_path = current_directory / 'client_secret_526155639435-ol30a40frn2bk3tmr60gmah7l55jbc33.apps.googleusercontent.com.json'
#     # OAuth flow to authenticate and get credentials
#     flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, SCOPES)
#     # Run the local server to get credentials
    
#     credentials = flow.run_local_server(port=8001)
#     print(credentials)

#     # Save credentials to session as JSON string
#     request.session['credentials'] = credentials.to_json()

#     # Redirect to the page where you fetch contacts
#     return redirect('import_google_contacts')
client_id = "526155639435-ol30a40frn2bk3tmr60gmah7l55jbc33.apps.googleusercontent.com"
client_secret = "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"
authorization_base_url = 'https://accounts.google.com/o/oauth2/auth'
token_url = 'https://accounts.google.com/o/oauth2/token'
grant_type = 'authorization_code'
scope = ['https://www.googleapis.com/auth/contacts.readonly']
# response_type = 'code'
from uuid import uuid4
from requests_oauthlib import OAuth2Session

def google_authenticate(request):
    redirect_uri = request.build_absolute_uri(reverse('google_authenticate_callback'))
    state = str(uuid4())

    # Step 1: User Authorization.
    google_client = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    authorization_url, state = google_client.authorization_url(authorization_base_url)
    print(authorization_url)
    # , response_type=response_type
    # State is used to prevent CSRF, keep this for later.
    request.session['oauth_state'] = state
    return redirect(authorization_url)

def google_authenticate_callback(request):
    # Step 2: User Authorization Callback.
    redirect_uri = request.build_absolute_uri(reverse('google_authenticate_callback'))
    google_client = OAuth2Session(client_id, redirect_uri=redirect_uri, state=request.session.get('oauth_state'))
    
    # Get the authorization response
    authorization_response = request.build_absolute_uri()
    
    # Fetch the access token
    token = google_client.fetch_token(token_url, authorization_response=authorization_response, client_secret=client_secret)

    # Save credentials to session or database as needed
    request.session['credentials'] = json.dumps(token)

    # Redirect to the page where you fetch contacts
    return redirect('import_google_contacts')

def import_google_contacts(request):
    # Fetch contacts using saved credentials
    credentials_json = request.session.get('credentials', None)
    print("Session credentials:", credentials_json)
    
    if credentials_json is None:
        # Redirect the user to authenticate if credentials are not present
        return redirect('google_authenticate')

    try:
        # Convert JSON string to dictionary
        credentials_info = json.loads(credentials_json)

        # Ensure that credentials_info is a dictionary
        if not isinstance(credentials_info, dict):
            # Handle the case where credentials_info is not a dictionary
            return HttpResponse("Invalid credentials format")
    except json.JSONDecodeError:
        return HttpResponse("Invalid JSON format")

    # Create Credentials object
    credentials = Credentials(
        token=credentials_info.get('token'),
        token_uri=credentials_info.get('token_uri'),
        client_id=credentials_info.get('client_id'),
        client_secret=credentials_info.get('client_secret'),
        scopes=credentials_info.get('scopes'),
        universe_domain=credentials_info.get('universe_domain'),
        expiry=credentials_info.get('expiry')
    )
    # Convert the expiry string to a datetime object
    credentials.expiry = datetime.strptime(credentials.expiry, "%Y-%m-%dT%H:%M:%S.%fZ")
    # If the credentials are expired, refresh them
    if credentials.expired:
        credentials.refresh(Request())

    # Build the Google Contacts API service
    service = build('people', 'v1', credentials=credentials)

    # Fetch the user's contacts
    results = service.people().connections().list(
        resourceName='people/me',
        pageSize=1000,
        personFields='names,emailAddresses,phoneNumbers,birthdays').execute()

    # Process the fetched contacts and store them in your Django models
    for person in results.get('connections', []):
        # Extract relevant information from the Google contact
        names = person.get('names', [])
        resources = person.get('resourceName',[])
        email_addresses = person.get('emailAddresses', [])
        phone_numbers = person.get('phoneNumbers', [])
        birthdays = person.get('birthdays', [])

        # Assume the first name is available
        first_name = names[0].get('givenName', '') if names else ''
        last_name = names[0].get('familyName', '') if names else ''

        # Assume the first email address and phone number are available
        email = email_addresses[0].get('value', '') if email_addresses else ''
        phone_number = phone_numbers[0].get('value', '') if phone_numbers else ''
        google_resource_id = resources

        # Assume the first birthday is available
        if isinstance(birthdays, list) and birthdays:
            # Take the first birthday from the list
            birthday_dict = birthdays[0]
            # Extract the date field from the birthday dictionary
            date_dict = birthday_dict.get('date', {})
            
            # Extract year, month, and day from the date dictionary
            year = date_dict.get('year')
            if year:
                year = year
            else:
                year = 2000
            month = date_dict.get('month', 1)
            day = date_dict.get('day', 1)

            # Check if all components are present
            if year and month and day:
                try:
                    birthday = datetime(year, month, day).date()
                except ValueError:
                    print(f"Invalid date components for birthday: {year}-{month}-{day}")
                    continue
            else:
                # Handle the case where some components are missing
                print("Incomplete date components in birthday dictionary")
                continue
        else:
            # Handle the case where 'birthdays' is not a list or is an empty list
            birthday = None
        # Create a new Client instance and save it to the database
        existing_clients = Clent.objects.filter(google_resource_id=google_resource_id, user=request.user)
        if existing_clients.exists():

            # Get the first object from the queryset
            existing_client = existing_clients.first()

            # Update existing client with the latest information
            existing_client.client_name = f"{first_name} {last_name}"
            existing_client.phone_number = phone_number
            existing_client.birthday = birthday
            # Update other fields as needed
            existing_client.save()
        else:
            # Create a new Client instance
            Clent.objects.create(
                user=request.user,
                client_name=f"{first_name} {last_name}",
                email=email,
                phone_number=phone_number,
                birthday=birthday,
                google_resource_id = google_resource_id,
                # Include other fields as needed
            )
    # Render a success page or redirect to another view
    # Add a success message
    messages.success(request, 'Google contacts successfully imported!')
    return redirect('client_list')

def settings(request):
    return render(request,'settings.html')

from django.core.mail import send_mail

def mail_send(request):
    if request.method =='POST':
        message_name = request.POST['message-name']
        message_email = request.POST['message-email']
        message = request.POST['message']
        message_to_email = request.POST['message-to-email']
        send_mail(
            message_name,
            message,
            message_email,
            [message_to_email],
        )

        return render(request, 'contact.html', {'message_name':message_name})

    else:
        return render(request, 'contact.html')
    
def add_event_type(request):
    if request.method == 'POST':
        form = EventTypeForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('events_list')
        else:
            print(form.errors)
    else:
        form = EventTypeForm()
    return render(request, 'add_event_type.html', {'form': form})



def event_types_list(request):
    event_types = event_type_model.objects.filter(user=request.user)
    return render(request, 'event_types_list.html', {'event_types': event_types})

def edit_event_type(request, event_type_id):
    event_types = get_object_or_404(event_type_model, id=event_type_id, user=request.user)

    if request.method == 'POST':
        form = EventTypeForm(request.POST, instance=event_types)
        if form.is_valid():
            form.save()
            return redirect('event_types_list')
    else:
        form = EventTypeForm(instance=event_types)

    return render(request, 'edit_event_type.html', {'event_type': event_types, 'form': form})

def delete_event_type(request, event_type_id):
    event_types = get_object_or_404(event_type_model, id=event_type_id, user=request.user)

    if request.method == 'POST':
        event_types.delete()
        return redirect('event_types_list')

    return render(request, 'delete_event_type.html', {'event_type': event_types})

def suggestions_link_settings(request):
    
    setups = get_object_or_404(suggestion_link_settings, user=request.user)

    if request.method == 'POST':
        form = suggestion_link_setup(request.POST, instance=setups)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = suggestion_link_setup(instance=setups)

    return render(request, 'edit_event_type.html', {'setups': setups, 'form': form})