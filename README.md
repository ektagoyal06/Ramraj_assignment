My name is Ekta
I have created this automation of:
Build a Python automation system that connects to:
 Gmail API
 Google Sheets API
The system must read real incoming emails from your own Gmail account and log
them into a Google Sheet. 

**Full description of project is as follows:**
**High-Level Architecture**
**Description:**
The system fetches unread emails from a Gmail account using the Gmail API, parses the content, and appends it to a Google Sheet via the Sheets API. It also marks the processed emails as read to prevent duplicates.

**Flow Overview:**

User authorizes the app via OAuth 2.0.

App fetches unread emails from Gmail.

Emails are parsed to extract sender, subject, date, and content.

Data is appended to a Google Sheet.

Processed emails are marked as read to avoid duplicate processing.

**Step-by-Step Setup Instructions**
**Clone the repository**

Copy code
git clone <repo-url>
cd gmail-to-sheets
Install Python dependencies

pip install -r requirements.txt
Required packages: google-api-python-client, google-auth-httplib2, google-auth-oauthlib, beautifulsoup4

**Create Google API Credentials**

Go to Google Cloud Console

Create a project and enable Gmail API and Google Sheets API.

Create OAuth 2.0 Client ID credentials for Desktop App.

**Download the JSON file and place it at:**

credentials/credentials.json
Update Google Sheet ID

Open your Google Sheet.

**Copy the Sheet ID from the URL:**

https://docs.google.com/spreadsheets/d/<SHEET_ID>/edit
Replace **SPREADSHEET_ID** in **sheets_service.py** with your Sheet ID.

Run the script

python src/main.py

Your browser will open a Google authorization screen.

Click Continue → Allow to give required permissions.

After successful authentication, **credentials/token.json** will be created.

Script will run: fetch emails, append data to Google Sheet, mark emails as read.

3. Explanation
OAuth Flow
Uses OAuth 2.0 Installed App flow.

Scopes requested:

https://www.googleapis.com/auth/gmail.modify → read and mark emails as read

https://www.googleapis.com/auth/spreadsheets → write data to Google Sheet

After first authorization, credentials are stored in token.json for reuse.

Duplicate Prevention Logic
After processing each email, it is marked as read:

gmail.users().messages().modify(userId="me", id=msg["id"], body={"removeLabelIds": ["UNREAD"]}).execute()
Only emails labeled as UNREAD are fetched, ensuring duplicates are not processed.

State Persistence Method
OAuth credentials are persisted in token.json.

This allows the script to run multiple times without re-authorizing, unless the token expires or is revoked.

4. Challenge Faced & Solution
Challenge: Gmail API emails come in HTML format, which included unwanted tags and styles when appended directly to Google Sheet.

Solution:

Used BeautifulSoup to parse HTML and extract clean text:

from bs4 import BeautifulSoup
soup = BeautifulSoup(html_body, "html.parser")
clean_text = soup.get_text()
Now the sheet contains readable content instead of full HTML.

5. Limitations
Works only for Gmail accounts.

Only fetches unread emails; already read emails are ignored.

HTML emails with complex formatting (tables, images) may lose structure.

Script currently runs locally; not deployed as a cloud service.

No automatic scheduling; requires manual execution or OS-level scheduler (e.g., cron or Task Scheduler).
