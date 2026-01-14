from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import os

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/spreadsheets"
]
TOKEN_PATH = "credentials/token.json"
CREDS_PATH = "credentials/credentials.json"  

SPREADSHEET_ID = "PASTE_YOUR_SPREADSHEET_ID_HERE"  

def get_credentials():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        if not creds.valid:
            os.remove(TOKEN_PATH)  
            creds = None

    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
        creds = flow.run_local_server(port=0)  
        with open(TOKEN_PATH, "w") as token_file:
            token_file.write(creds.to_json())

    return creds

def get_sheets_service():
    creds = get_credentials()
    return build("sheets", "v4", credentials=creds)

def append_row(service, row):
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="Sheet1!A:D",
        valueInputOption="RAW",
        body={"values": [row]},
    ).execute()

