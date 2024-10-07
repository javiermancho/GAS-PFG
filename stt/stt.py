from flask import Flask, request, jsonify
import io
from google.cloud import speech
from google.oauth2 import service_account
from dotenv import load_dotenv

import os
import requests
import mysql.connector
import pandas as pd
import json

load_dotenv()
client_file = os.getenv("STT_PATH_FILE")

app = Flask("Speech-To-Text")

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
    

@app.route("/audios", methods=["GET"])
def get_audios():
    mydb = mysql.connector.connect(
        host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        database = os.getenv("DB_NAME")
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM audios")
    myresult = mycursor.fetchall()
    mydb.close()
    return jsonify({"response": myresult})


if __name__ == "__main__":
    app.run(host= "0.0.0.0", port=5001, debug=True)
