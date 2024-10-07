import pandas as pd

import numpy as np

# StreamLit Components
import streamlit as st
# Audio Recorder
from audio_recorder_streamlit import audio_recorder
# AwsomeTable


import requests
import json

### APP ###
st.title("Voice Recognition")
st.write("Press the button and speak to the microphone")

def send_audio_to_server(audio_bytes):
    url = "http://stt:5001/stt"
    response = requests.post(url, files={"audio": audio_bytes})
    data = response.json()
    return data.get("response")


def get_audios():
    url = "http://stt:5001/audios"
    response = requests.get(url)
    # Return type: { "response": [ [ 1, "test", "test" ] ] }
    # We need to convert it to a DataFrame
    data = response.json()
    data = data.get("response")
    data = pd.DataFrame(data, columns=["id", "name", "description"])
    return data


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


st.write("Saved responses:")
#grid for responses

data = get_audios()
st.dataframe(data, hide_index=True, key = "id", width=None, use_container_width=False)
