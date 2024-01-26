# crm/email_backend.py

from django.core.mail.backends.smtp import EmailBackend
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

class GmailOAuth2EmailBackend(EmailBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.gmail_client_id = kwargs.get('GMAIL_CLIENT_ID')
        self.gmail_client_secret = kwargs.get('GMAIL_CLIENT_SECRET')
        self.gmail_refresh_token = kwargs.get('GMAIL_REFRESH_TOKEN')
        self.gmail_user = kwargs.get('GMAIL_USER')

        self.credentials = self.get_credentials()

    def get_credentials(self):
        credentials = Credentials.from_authorized_user_file('token.json', self.scopes)
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secret.json', self.scopes)
                credentials = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(credentials.to_json())
        return credentials

    def open(self):
        if self.connection:
            return False

        self.connection = self.get_credentials()
        return True
