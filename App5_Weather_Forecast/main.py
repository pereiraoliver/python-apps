import backend
import plotly.express as px
import streamlit as st

# Add title, text input, slider, select box, and sub header
st.title("Weather Forecast for the Next Days")
place = st.text_input("Place: ")
days = st.slider(
    "Forecast Days",
    min_value=1,
    max_value=5,
    help="Select the number of forecasted days",
)

option = st.selectbox("Select data to view", ("Temperature", "Sky"))
st.subheader(f"{option} for the next {days} days in {place}")
# Get the temperature/sky data
try:
    if place:
        filtered_data = backend.get_data(place, days)
        match option:
            case "Temperature":
                temperature = [
                    float(dict["main"]["temp"]) / 10 for dict in filtered_data
                ]
                date = [dict["dt_txt"] for dict in filtered_data]
                # Create a temperatureplot
                figure = px.line(
                    x=date, y=temperature, labels={"x": "Date", "y": "Temerature (C)"}
                )
                st.plotly_chart(figure)
            case "Sky":
                sky_conditions = [dict["weather"][0]["main"] for dict in filtered_data]
                date = [dict["dt_txt"] for dict in filtered_data]
                images = {
                    "Clouds": "downloads/cloud.png",
                    "Rain": "downloads/rain.png",
                    "Clear": "downloads/clear.png",
                    "Snow": "downloads/snow.png",
                }
                for i in range(0, len(sky_conditions), 6):
                    cols = st.columns(6)
                    for col, image, dt in zip(
                        cols, sky_conditions[i : i + 6], date[i : i + 6]
                    ):
                        with col:
                            st.image(images[image], use_container_width=True)
                            st.write(dt)
except KeyError:
    st.write("That place does not exist. Try Again!")
