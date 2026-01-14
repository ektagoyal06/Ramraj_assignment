from bs4 import BeautifulSoup

def parse_email(service, msg_id):
    message = service.users().messages().get(userId="me", id=msg_id, format="full").execute()

    headers = message["payload"]["headers"]
    subject = next(h["value"] for h in headers if h["name"] == "Subject")
    sender = next(h["value"] for h in headers if h["name"] == "From")
    date = next(h["value"] for h in headers if h["name"] == "Date")

  
    parts = message["payload"].get("parts", [])
    body = ""
    for part in parts:
        if part["mimeType"] == "text/plain":
            body = part["body"]["data"]
            break
        elif part["mimeType"] == "text/html":
            html = part["body"]["data"]
            soup = BeautifulSoup(html, "html.parser")
            body = soup.get_text()
            break

  
    import base64
    body = base64.urlsafe_b64decode(body.encode("UTF-8")).decode("UTF-8")

    return sender, subject, date, body

