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
import base64
from email.mime.text import MIMEText
from io import BytesIO
import env

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
        env.set("FOLDER", folder.get("id"))
    except HttpError as error:
        print(error)
        return False
    return True


'''
'''


def create_file():
    try:
        creds = Credentials.from_authorized_user_file('keys/token.json', SCOPES)
        service_drive = build('drive', 'v3', credentials=creds)
        file_metadata = {
            "name": "secrets.txt",
            "parents": [env.get("FOLDER")]
        }
        media = MediaFileUpload(env.get("ENCF"), resumable=False)
        file = service_drive.files().create(body=file_metadata, media_body=media, fields='id').execute()
        env.set("GFILE", file.get("id"))

    except HttpError as error:
        print(error)
        return False
    return True



def remove_file_encf():
    try:
        os.remove(env.get("ENCF"))
        env.unset("ENCF")
    except:
        pass
    finally: 
        pass

def remove_file_decf():
    try:
        os.remove(env.get('DECF'))
        env.unset('DECF')
    except:
        pass
    finally:
        pass

'''
'''

def upload_file():
    try:
        creds = Credentials.from_authorized_user_file('keys/token.json', SCOPES)
        service_drive = build('drive', 'v3', credentials=creds)
        media = MediaFileUpload(env.get("ENCF"), resumable=True)
        file = service_drive.files().update(fileId=env.get("GFILE"), media_body=media).execute()
        #os.remove(env.get("ENCF"))
        #env.unset("ENCF")

    except HttpError as error:
        print(error)
    return


'''
'''


def download_file():
    try:
        creds = Credentials.from_authorized_user_file('keys/token.json', SCOPES)
        service_drive = build('drive', 'v3', credentials=creds)
        env.set("ENCF", "outputs/download.enc")
        file = open(env.get("ENCF"), 'wb')
        fh = io.BytesIO()
        request = service_drive.files().get_media(fileId=env.get("GFILE"))
        download = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = download.next_chunk()
            print ("Download %d%%." % int(status.progress() * 100))
        file.write(fh.getbuffer())
        file.close()
    except HttpError as error:
        print(error)
        env.unset('GFILE')
        env.unset('FOLDER')
        return False
    except:
        env.unset('GFILE')
        env.unset('FOLDER')
    else:
        return True


'''TODO share file, update file permissions, revoke file permissions'''


def build_message(receiver, shamir_key):
    message_text = "A new Shamir secret key has been shared with you by " + env.get("SENDER") + ". \
     Please keep it in a safe place! \n\nKey:  " + shamir_key
    subject = "New Shamir Key Share"
    message = MIMEText(message_text)
    message['to'] = receiver
    message['from'] = env.get("SENDER")
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


'''
'''


def send_shamir():
    try:
        creds = Credentials.from_authorized_user_file('keys/token.json', SCOPES)
        service_mail = build('gmail', 'v1', credentials=creds)
        profile = service_mail.users().getProfile(userId='me').execute()
        env.set("SENDER", profile.get('emailAddress'))
        r = json.loads(env.get("RECEIVERS"))
        s = json.loads(env.get("SHARES"))
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
