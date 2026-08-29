import os
import smtplib
import ssl
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()

GMAIL = os.getenv("GMAIL")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


def send_email(content):
    message = EmailMessage()
    message["From"] = GMAIL
    message["To"] = GMAIL
    message["Subject"] = content
    message.set_content(content)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(GMAIL, GMAIL_APP_PASSWORD)
        server.send_message(message)

    print("Email Sent!")
