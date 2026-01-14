from gmail_service import get_gmail_service, fetch_unread_emails
from email_parser import parse_email
from sheets_service import get_sheets_service, append_row


def main():
    gmail = get_gmail_service()
    sheets = get_sheets_service()

    messages = fetch_unread_emails(gmail)

    for msg in messages:
        sender, subject, date, body = parse_email(gmail, msg["id"])
        append_row(sheets, [sender, subject, date, body])

        gmail.users().messages().modify(
            userId="me",
            id=msg["id"],
            body={"removeLabelIds": ["UNREAD"]}
        ).execute()


if __name__ == "__main__":
    main()
