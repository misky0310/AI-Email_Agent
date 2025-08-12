import imaplib
import email
from email.header import decode_header
from email_handling.clean_body import clean_email_body

def fetch_emails(server, user, password, n=10):
    try:
        mail = imaplib.IMAP4_SSL(server)
        mail.login(user, password)
        mail.select('inbox')

        status, msgs = mail.search(None, "UNSEEN")
        if status != 'OK':
            print("No messages found!")
            return []

        email_ids = msgs[0].split()
        emails = []
        seen_keys = set()  # For deduplication

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

                    # Extract From and Date (normalize to string)
                    from_addr = msg.get("From", "").strip()
                    date_str = msg.get("Date", "").strip()

                    # Create dedup key
                    dedup_key = (subject, from_addr, date_str)
                    if dedup_key in seen_keys:
                        continue
                    seen_keys.add(dedup_key)

                    # Extract body
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

                    # Clean the email body
                    clean_body = clean_email_body(body)

                    emails.append({
                        "Subject": subject,
                        "Body": clean_body,
                        "From": from_addr,
                        "Date": date_str
                    })

        mail.logout()

        # Print final deduplicated subjects
        for e in emails:
            print("Subject:", e["Subject"])

        return emails

    except imaplib.IMAP4.error as e:
        print("IMAP error:", str(e))
        return []
    except Exception as e:
        print("General error:", str(e))
        return []
