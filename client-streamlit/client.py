import streamlit as st
import pandas as pd
import numpy as np
from audio_recorder_streamlit import audio_recorder
import requests
import json

### STYLES ###
st.markdown(
    """
    <style>
    .background {
        background-color: #f0f5f5;
    }
    </style>
    """,
    unsafe_allow_html=True
)
### APP ###
st.title("Voice Recognition")
st.write("Press the button and speak to the microphone")

def send_audio_to_server(audio_bytes):
    url = "http://stt:5001/stt"
    response = requests.post(url, files={"audio": audio_bytes})
    data = response.json()
    return data.get("response")

if 'responses' not in st.session_state:
    st.session_state['responses'] = []


audio_bytes = audio_recorder(
    text = "",
    recording_color = "ffffff",
    neutral_color = "add8e6",
    icon_name = "microphone",
)
if audio_bytes:
    #st.audio(audio_bytes, format="audio/wav")
    response = send_audio_to_server(audio_bytes)
    st.session_state['responses'].append(response)


st.write("Previous responses:")
#grid for responses
st.dataframe(pd.DataFrame(st.session_state['responses'], columns=["Responses"]), hide_index=True, width=1000)

