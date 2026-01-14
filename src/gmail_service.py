import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# ✅ Include both Gmail and Sheets scopes
SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/spreadsheets"
]

TOKEN_PATH = "credentials/token.json"
CREDS_PATH = "credentials/credentials.json"


def get_gmail_service():
    creds = None

    # 🔹 Load token if it exists
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        # 🔹 Delete old token if it's invalid
        if not creds.valid:
            os.remove(TOKEN_PATH)
            creds = None

    # 🔹 Create new token if needed
    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    # 🔹 Build Gmail service
    service = build("gmail", "v1", credentials=creds)
    return service


def fetch_unread_emails(service):
    results = service.users().messages().list(
        userId="me",
        q="is:unread in:inbox"
    ).execute()

    return results.get("messages", [])
