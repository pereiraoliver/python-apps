import os
import smtplib
from email.mime.text import MIMEText

import requests
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GMAIL = os.getenv("GMAIL")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
US_DOMAINS = os.getenv("US_DOMAINS")

# Get news
url = "https://newsapi.org/v2/everything"
params = {
    "domains": US_DOMAINS,
    "language": "en",
    "sortBy": "publishedAt",
    "pageSize": 20,
    "apiKey": NEWS_API_KEY,
}

request = requests.get(url, params=params)

data = request.json()

# AI summarizing the news
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

model = init_chat_model(
    model="gpt-5.6-luna", model_provider="openai", api_key=OPENAI_API_KEY
)

prompt = f"""
You are a news summarizer. Write a short paragraph and summarize the following news articles.
News articles: {data["articles"]}
Provide another paragraph with how these articles affect the stock market.
"""

response = model.invoke(prompt)
response_str = response.content
print(response_str)

# Build email
para = response_str.split("\n\n")
body = "<h2>Oliver's US Conservative News</h2>"
body += "".join(f"<p>{p}</p>" for p in para)

# Send email
email = MIMEText(body, "html")
email["Subject"] = "Oliver's US Conservative News"
email["From"] = GMAIL
email["To"] = GMAIL

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(GMAIL, GMAIL_APP_PASSWORD)
    server.send_message(email)

print("Email sent!")
