from flask import Flask, request, jsonify
import io
from google.cloud import speech
from google.oauth2 import service_account
import os
import requests
import mysql.connector
import pandas as pd
import json

app = Flask("Speech-To-Text")

client_file = "credentials.json"
credentials = service_account.Credentials.from_service_account_file(client_file)
client = speech.SpeechClient(credentials = credentials)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    #sample_rate_hertz=44100,
    language_code="en",
    audio_channel_count=2
)

@app.route("/stt", methods=["POST"])
def stt():
    audio = request.files["audio"].read()
    audio = speech.RecognitionAudio(content=audio)
    response = client.recognize(config=config, audio=audio)
    response_text = ""
    for result in response.results:
        response_text = response_text + result.alternatives[0].transcript
    return jsonify({"response": response_text})
    

if __name__ == "__main__":
    app.run(host= "0.0.0.0", port=5001, debug=True)
