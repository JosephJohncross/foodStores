import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pickle
import os
import django
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from food_stores.settings import  BASE_DIR, SCOPES
from django.contrib.staticfiles.storage import staticfiles_storage

url = staticfiles_storage.url('client_secret.json')

def get_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(url, SCOPES)
            creds = flow.run_local_server(port=8001)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    return service


def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id,
                body=message).execute()

        print('Message Id: {}'.format(message['id']))

        return message
    except Exception as e:
        return None

def create_message_with_attachment(sender,to,subject,message_text,):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    raw_message = \
        base64.urlsafe_b64encode(message.as_string().encode('utf-8'))
    return {'raw': raw_message.decode('utf-8')}
 

def sendingMessage(msgto,subject,message):
    service = get_service()
    user_id = 'me'
    msg = create_message_with_attachment(f'<email-from>, <{msgto}>, <{subject}> ,<{message}>')
    send_message(service, user_id, msg)