import time
from datetime import datetime
from zoneinfo import ZoneInfo

import cv2
import streamlit as st

st.title("Motion Detector")
start = st.button("Start Camera")
now = datetime.now(ZoneInfo("Asia/Kolkata"))

if start:
    streamlit_image = st.image([])
    camera = cv2.VideoCapture(0)

    while True:
        tm = now.strftime("%H:%M:%S")
        weekday = now.strftime("%A")

        check, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        cv2.putText(
            img=frame,
            text=weekday,
            org=(35, 25),
            fontFace=cv2.FONT_HERSHEY_PLAIN,
            fontScale=1,
            color=(255, 255, 255),
            thickness=1,
            lineType=cv2.LINE_AA,
        )

        cv2.putText(
            img=frame,
            text=tm,
            org=(35, 50),
            fontFace=cv2.FONT_HERSHEY_PLAIN,
            fontScale=1,
            color=(255, 0, 0),
            thickness=1,
            lineType=cv2.LINE_AA,
        )

        streamlit_image.image(frame)
