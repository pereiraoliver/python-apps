import os
from datetime import datetime, timezone

import plotly.express as px
import streamlit as st
from nltk.sentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
sentiment = analyzer.polarity_scores(
    "Hey, look how beautiful the trees are. I love them. I really love them"
)

files = sorted(os.listdir("downloads"))
data = {"date": [], "possitivity": [], "negativity": []}

for file in files:
    conv_date = datetime.strptime(file.split(".")[0], "%Y-%m-%d").replace(
        tzinfo=timezone.utc
    )
    date = conv_date.strftime("%b %d %Y")
    data["date"].append(date)
    with open(f"downloads/{file}") as file:
        diary = file.read()
    senti = analyzer.polarity_scores(diary)
    data["possitivity"].append(senti["pos"])
    data["negativity"].append(senti["neg"])

st.header("Diary Tone")
st.subheader("Positivity")
fig1 = px.line(
    x=data["date"],
    y=data["possitivity"],
    labels={"x": "Date", "y": "Possitivity"},
)
st.plotly_chart(fig1, use_container_width=True)
st.subheader("Negativity")
fig2 = px.line(
    x=data["date"], y=data["negativity"], labels={"x": "Date", "y": "Negativity"}
)
st.plotly_chart(fig2, use_container_width=True)
