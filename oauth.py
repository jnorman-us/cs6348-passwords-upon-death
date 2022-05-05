from __future__ import print_function

import io
import os.path
import json
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from dotenv import set_key, unset_key, get_key
import base64
from email.mime.text import MIMEText
from io import BytesIO

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com', 'https://www.googleapis.com/auth/drive.file']


'''
'''


def create_folder():
    try:
        creds = Credentials.from_authorized_user_file('keys/token.json', SCOPES)
        service_drive = build('drive', 'v3', credentials=creds)
        folder_metadata = {
            "name": "ShamirPasswords",
            "mimeType": "application/vnd.google-apps.folder"
        }
        folder = service_drive.files().create(body=folder_metadata, fields="id").execute()
        set_key("persist.env", "FOLDER", folder.get("id"))
    except HttpError as error:
        print(error)

    return


'''
'''


def create_file():
    try:
        creds = Credentials.from_authorized_user_file('keys/token.json', SCOPES)
        service_drive = build('drive', 'v3', credentials=creds)
        file_metadata = {
            "name": "secrets.txt",
            "parents": [get_key("persist.env", "FOLDER")]
        }
        media = MediaFileUpload(get_key("persist.env", "ENCF"), resumable=False)
        file = service_drive.files().create(body=file_metadata, media_body=media, fields='id').execute()
        set_key("persist.env", "GFILE", file.get("id"))

    except HttpError as error:
        print(error)
    return



def remove_file_encf():
    os.remove(get_key("persist.env", "ENCF"))
    unset_key("persist.env", "ENCF")

'''
'''

def upload_file():
    try:
        creds = Credentials.from_authorized_user_file('keys/token.json', SCOPES)
        service_drive = build('drive', 'v3', credentials=creds)
        media = MediaFileUpload(get_key("persist.env", "ENCF"), resumable=True)
        file = service_drive.files().update(fileId=get_key("persist.env", "GFILE"), media_body=media).execute()
        os.remove(get_key("persist.env", "ENCF"))
        unset_key("persist.env", "ENCF")

    except HttpError as error:
        print(error)
    return


'''
'''


def download_file():
    try:
        creds = Credentials.from_authorized_user_file('keys/token.json', SCOPES)
        service_drive = build('drive', 'v3', credentials=creds)
        set_key("persist.env", "ENCF", "outputs/download.enc")
        file = open(get_key("persist.env", "ENCF"), 'wb')
        fh = io.BytesIO()
        request = service_drive.files().get_media(fileId=get_key("persist.env", "GFILE"))
        download = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = download.next_chunk()
            print ("Download %d%%." % int(status.progress() * 100))
        file.write(fh.getbuffer())
    except HttpError as error:
        print(error)
    return


'''TODO share file, update file permissions, revoke file permissions'''


def build_message(receiver, shamir_key):
    message_text = "A new Shamir secret key has been shared with you by " + get_key("persist.env",  "SENDER") + ". \
     Please keep it in a safe place! \n\nKey:  " + shamir_key
    subject = "New Shamir Key Share"
    message = MIMEText(message_text)
    message['to'] = receiver
    message['from'] = get_key("persist.env", "SENDER")
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


'''
'''


def send_shamir():
    try:
        creds = Credentials.from_authorized_user_file('keys/token.json', SCOPES)
        service_mail = build('gmail', 'v1', credentials=creds)
        profile = service_mail.users().getProfile(userId='me').execute()
        set_key("persist.env", "SENDER", profile.get('emailAddress'))
        receivers = get_key("persist.env", "RECEIVERS")
        shamir_keys = get_key("persist.env", "SHARES")
        r = receivers.split(", ")
        s = shamir_keys.split(" ")
        for x in range(len(r)):
            service_mail.users().messages().send(userId="me", body=build_message(r[x], s[x])).execute()

    except HttpError as error:
        print(error)
    return


'''
'''


def getAuth():
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
    creds = None

    if os.path.exists('keys/token.json'):
        creds = Credentials.from_authorized_user_file('keys/token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'keys/client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('keys/token.json', 'w') as token:
            token.write(creds.to_json())
    return
