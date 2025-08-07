import imaplib
import email
from email.header import decode_header
from email_handling.clean_body import  clean_email_body

def fetch_emails(server, user, password, n=10):
    try:
        # Connect securely to the IMAP server
        mail = imaplib.IMAP4_SSL(server)
        mail.login(user, password)
        mail.select('inbox')

        # Search all emails in the inbox
        status, msgs = mail.search(None, "UNSEEN")
        if status != 'OK':
            print("No messages found!")
            return []

        email_ids = msgs[0].split()

        emails = []

        # Fetch the latest n emails
        for eid in reversed(email_ids[-n:]):
            res, msg_data = mail.fetch(eid, "(RFC822)")
            if res != 'OK':
                continue

            for response in msg_data:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])

                    # Decode subject
                    raw_subject = decode_header(msg["Subject"])[0]
                    subject = raw_subject[0].decode() if isinstance(raw_subject[0], bytes) else raw_subject[0]

                    # Get email body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))

                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                try:
                                    body = part.get_payload(decode=True).decode(errors="ignore")
                                    break
                                except:
                                    pass
                    else:
                        body = msg.get_payload(decode=True).decode(errors="ignore")

                    #clean the email body
                    clean_body = clean_email_body(body)

                    # Append structured email content
                    emails.append({
                        "Subject":subject,
                        "Body": clean_body,
                        "From": msg["From"],
                        "Date": msg["Date"]
                    })

        mail.logout()
        return emails

    except imaplib.IMAP4.error as e:
        print("IMAP error:", str(e))
        return []
    except Exception as e:
        print("General error:", str(e))
        return []
