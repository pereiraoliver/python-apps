from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import plotly.express as px
import requests
import selectorlib
import streamlit as st

URL = "https://programmer100.pythonanywhere.com/"
BASE_DIR = Path(__file__).resolve().parent

response = requests.get(URL)
source = response.text
extractor = selectorlib.Extractor.from_yaml_file(BASE_DIR / "scrap.yaml")
value = extractor.extract(source)["temp"]

with open("data.txt", "+a") as file:
    now = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%y-%m-%d-%H-%M-%S")
    val = now + "," + value
    file.write(val + "\n")

temp = []
date = []

with open(BASE_DIR / "data.txt", "r") as file:
    data = file.readlines()
    data.pop(0)
    for d in data:
        data = d.split(",")
        date.append(data[0])
        temp.append(data[1].strip("\n"))

print(date)
print(temp)

fig1 = px.line(
    x=date,
    y=temp,
    labels={"x": "Date", "y": "Temperature(C)"},
)
st.plotly_chart(fig1, use_container_width=True)
