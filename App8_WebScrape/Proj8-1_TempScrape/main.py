import sqlite3
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import plotly.express as px
import requests
import selectorlib
import streamlit as st

URL = "https://programmer100.pythonanywhere.com/"
BASE_DIR = Path(__file__).resolve().parent

connection = sqlite3.connect(BASE_DIR.parent / "data.db")
connection.execute("CREATE TABLE IF NOT EXISTS temps (date TEXT, temp INTEGER)")
connection.commit()

response = requests.get(URL)
source = response.text
extractor = selectorlib.Extractor.from_yaml_file(BASE_DIR / "scrap.yaml")

extracted = extractor.extract(source)["temp"]
now = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%y-%m-%d-%H-%M-%S")

cursor = connection.cursor()
cursor.execute("INSERT INTO temps VALUES (?, ?)", [now, extracted])
connection.commit()

cursor = connection.cursor()
cursor.execute("SELECT * FROM temps ORDER BY date DESC LIMIT 10")
rows = cursor.fetchall()

date = [r[0] for r in rows]
temp = [r[1] for r in rows]

print(date)
print(temp)

fig1 = px.line(
    x=date,
    y=temp,
    labels={"x": "Date", "y": "Temperature(C)"},
)
st.plotly_chart(fig1, use_container_width=True)
