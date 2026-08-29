import pandas as pd
import plotly.express as px
import streamlit as st

df = pd.read_csv("downloads/happy.csv")

st.title("In Search of Happiness")

optX = st.selectbox(
    "Select data for the X-axis",
    (
        "GDP",
        "Happiness",
        "Generosity",
        "Social Support",
        "Life Expectancy",
        "Freedom of Choice",
        "Corruption",
    ),
)
optY = st.selectbox(
    "Select data for the Y-axis",
    (
        "GDP",
        "Happiness",
        "Generosity",
        "Social Support",
        "Life Expectancy",
        "Freedom of Choic",
        "Corruption",
    ),
)

st.subheader(f"{optX} and {optY}")


def get_list(input):
    match input:
        case "GDP":
            col = "gdp"
        case "Happiness":
            col = "happiness"
        case "Generosity":
            col = "generosity"
        case "Social Support":
            col = "social_support"
        case "Life Expectancy":
            col = "life_expectancy"
        case "Freedom of Choice":
            col = "freedom_to_make_life_choices"
        case "Corruption":
            col = "corruption"
    return df[col].tolist()


listX = get_list(optX)
listY = get_list(optY)

figure = px.scatter(x=listX, y=listY, labels={"x": optX, "y": optY})

st.plotly_chart(figure)
