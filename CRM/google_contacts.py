from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']

def get_google_contacts(request):
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret_526155639435-ol30a40frn2bk3tmr60gmah7l55jbc33.apps.googleusercontent.com.json', SCOPES)
    credentials = flow.run_local_server(port=0)

    # Save the credentials to the session for later use
    request.session['credentials'] = credentials.to_json()

    # Now you can use the credentials to fetch contacts


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from django.shortcuts import redirect
from .models import Clent

def get_google_contacts(request):
    credentials_json = request.session.get('credentials', None)
    if credentials_json is None:
        # Redirect the user to authenticate if credentials are not present
        return redirect('google_authenticate')

    credentials = Credentials.from_json(credentials_json)

    # If the credentials are expired, refresh them
    if credentials.expired:
        credentials.refresh(Request())

    # Build the Google Contacts API service
    service = build('people', 'v1', credentials=credentials)

    # Fetch the user's contacts
    results = service.people().connections().list(
        resourceName='people/me',
        pageSize=10,
        personFields='names,emailAddresses,phoneNumbers').execute()

    # Process the fetched contacts and store them in your Django models
    for person in results.get('connections', []):
        # Extract relevant information from the Google contact
        names = person.get('names', [])
        email_addresses = person.get('emailAddresses', [])
        phone_numbers = person.get('phoneNumbers', [])

        # Assume the first name is available
        first_name = names[0].get('givenName', '') if names else ''
        last_name = names[0].get('familyName', '') if names else ''

        # Assume the first email address and phone number are available
        email = email_addresses[0].get('value', '') if email_addresses else ''
        phone_number = phone_numbers[0].get('value', '') if phone_numbers else ''

        # Create a new Client instance and save it to the database
        Clent.objects.create(
            user=request.user,  # Assuming you have a user associated with the contacts
            client_name=f"{first_name} {last_name}",
            email=email,
            phone_number=phone_number,
            # Include other fields as needed
        )