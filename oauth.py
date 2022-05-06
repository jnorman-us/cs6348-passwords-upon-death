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
import env

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com', 'https://www.googleapis.com/auth/drive.file']


''' 
    create_folder() creates a new folder in the users google drive
    titled "ShamirPasswords" and stores the folderid in .env as "FOLDER"
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
    create_file() creates a new file titled 'secrets.txt' in the users designated google drive folder
    using the folder id from .env "FOLDER"; stores the new file id in .env "GFILE"
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


''' 
    get_gfile_permisions 
    returns a permissions resource
    from the oauth and fileid attributes
    USED FOR TESTING VERIFICATION ONLY
'''


def get_gfile_permissions():
    try:
        creds = Credentials.from_authorized_user_file('keys/token.json', SCOPES)
        service_drive = build('drive', 'v3', credentials=creds)
        perms = service_drive.permissions().list(fileId=env.get("GFILE")).execute()

    except HttpError as error:
        print(error)
    return perms


'''
    share_gfile() shares the users designated google secrets.txt file (in encrypted format)
    with the user supplied email addresses for shamir keys.  Currently, there is no way to verify 
    if these email addresses are valid
'''


def share_gfile():
    try:
        creds = Credentials.from_authorized_user_file('keys/token.json', SCOPES)
        service_drive = build('drive', 'v3', credentials=creds)
        receivers = env.get("RECEIVERS")
        rx = receivers.split(" ", -1)
        for rcp in rx:
            grant = {'role': 'writer', 'type': 'user', 'emailAddress': rcp}
            perms = service_drive.permissions().create(fileId=env.get("GFILE"), body=grant).execute()

    except HttpError as error:
        print(error)
    return


'''
    remove_file_encf() removes the local copy of the encrypted file and resets
    the file name of .env "ENCF" to null
'''


def remove_file_encf():
    try:
        os.remove(env.get("ENCF"))
        env.unset("ENCF")
    except:
        pass
    finally: 
        pass


'''
    remove_file_decf() removes the local copy of the encrypted file and resets
    the file name of .env "DECF" to null
'''


def remove_file_decf():
    try:
        os.remove(env.get('DECF'))
        env.unset('DECF')
    except:
        pass
    finally:
        pass


''' 
    upload_file() overwrites the existing google drive doc secrets.txt with the newly encrypted information
'''


def upload_file():
    try:
        creds = Credentials.from_authorized_user_file('keys/token.json', SCOPES)
        service_drive = build('drive', 'v3', credentials=creds)
        media = MediaFileUpload(env.get("ENCF"), resumable=True)
        file = service_drive.files().update(fileId=env.get("GFILE"), media_body=media).execute()

    except HttpError as error:
        print(error)
    return


'''
    download_fil() downloads the encrypted google drive doc secrets.txt from the users drive
    using .env "GFILE" for file id, and stores locally in outputs/download.enc
'''

'''TODO does this work as is, or do we need to create the outputs folder first?'''
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
            #print ("Download %d%%." % int(status.progress() * 100))
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


'''
    TODO:
    destroy_gfile() deletes the users (possibly shared) google drive file called
    secrets.txt.  Should be called if the user decides to change receipients, etc.
'''


def destroy_gfile():
    try:
        creds = Credentials.from_authorized_user_file('keys/token.json', SCOPES)
        service_drive = build('drive', 'v3', credentials=creds)
        empty = service_drive.files().delete(fileId=env.get("GFILE")).execute()
        print(empty)
    except HttpError as error:
        print(error)
    return


'''
    build_message() uses the receipient's email address and the generated shamir key to
    formate a gmail message in order to send the key to the receipient
'''


def build_message(receiver, shamir_key):
    message_text = "A new Shamir secret key has been shared with you by " + get_key("persist.env",  "SENDER") + ". \
     Please keep it in a safe place! \n\nKey:  " + shamir_key
    subject = "New Shamir Key Share"
    message = MIMEText(message_text)
    message['to'] = receiver
    message['from'] = env.get("SENDER")
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


'''
    send_shamir() parses .env "RECEIVERS" and "SHARES" for the tuple of
    receipient, shamir_key in order to email the designated receipients the keys
'''


def send_shamir():
    try:
        creds = Credentials.from_authorized_user_file('keys/token.json', SCOPES)
        service_mail = build('gmail', 'v1', credentials=creds)
        profile = service_mail.users().getProfile(userId='me').execute()
        env.set("SENDER", profile.get('emailAddress'))
        receivers = env.get("RECEIVERS")
        shamir_keys = env.get("SHARES")
        r = receivers.split(" ")
        s = shamir_keys.split(" ")
        for x in range(len(r)):
            service_mail.users().messages().send(userId="me", body=build_message(r[x], s[x])).execute()

    except HttpError as error:
        print(error)
    return


'''
    getAuth() is oauth login for apis, stores token in 
    keys/token.json
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
