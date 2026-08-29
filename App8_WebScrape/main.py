import sqlite3
import time
from pathlib import Path

import requests
import selectorlib
from send_email import send_email

BASE_DIR = Path(__file__).resolve().parent

connection = sqlite3.connect(BASE_DIR / "data.db")

URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}


def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url, HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file(BASE_DIR / "extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES (?,?,?)", row)
    connection.commit()


def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM events WHERE band=? AND city =? AND date =?", (band, city, date)
    )
    rows = cursor.fetchall()
    return rows


count = 0
if __name__ == "__main__":
    while count < 5:
        scrapped = scrape(URL)
        extracted = extract(scrapped)
        print(extracted)

        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row:
                data = store(extracted)
                send_email(f"New Event Alert! {extracted}")
            else:
                print("Already exists!")
        time.sleep(2)
        count += 1
