import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv
from PIL import Image

load_dotenv()

GMAIL = os.getenv("GMAIL")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


def send_email(image_path, clean_folder):
    print("send_email function started")
    email_message = EmailMessage()
    email_message["Subject"] = "New customer showed up!"
    email_message["From"] = GMAIL
    email_message["To"] = GMAIL
    email_message.set_content("Hey, we just have a new customer!!")

    with open(image_path, "rb") as file:
        content = file.read()

    with Image.open(image_path) as image:
        image_type = image.format.lower()

    email_message.add_attachment(content, maintype="image", subtype=image_type)

    with smtplib.SMTP("smtp.gmail.com", 587) as gmail:
        gmail.ehlo()
        gmail.starttls()
        gmail.login(GMAIL, GMAIL_APP_PASSWORD)
        gmail.send_message(email_message)

    print("send_email function ended")
    clean_folder()


if __name__ == "__main__":
    send_email("downloads/19.png")
