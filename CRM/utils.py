# contacts/utils.py
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from .models import Clent
from datetime import datetime


SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']

def authenticate_with_google():
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret_526155639435-ol30a40frn2bk3tmr60gmah7l55jbc33.apps.googleusercontent.com.json',  )
    credentials = flow.run_local_server(port=0)
    return credentials

def get_google_contacts(credentials):
    service = build('people', 'v1', credentials=credentials)
    results = service.people().connections().list(
        resourceName='people/me',
        personFields='names,emailAddresses,phoneNumbers,birthdays').execute()
    connections = results.get('connections', [])
    return connections


def save_contacts_to_django(connections):
    for person in connections:
        name = person.get('names', [{}])[0].get('displayName', '')
        email = person.get('emailAddresses', [{}])[0].get('value', '')
        phone_number = person.get('phoneNumbers', [{}])[0].get('value', '')
        birthday = person.get('birthdays', [{}])[0].get('date', '')

        # Convert birthday to a valid date format (if available)
        if birthday:
            birthday = datetime.strptime(birthday, '%Y-%m-%d').date()

        # Ensure that the data is valid before creating the model instance
        if name and (email or phone_number):
            Clent.objects.create(
                client_name=name,
                email=email,
                phone_number=phone_number,
                birthday=birthday
            )