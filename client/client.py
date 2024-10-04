from flask import Flask, request
import requests
import os
import io

app = Flask("Client")

sample_audios = [".sample-audios/harvard.wav", 
                 ".sample-audios/javier.wav", 
                 ".sample-audios/cesar.wav"]


@app.route("/client", methods=["POST"])
def client():
    response = requests.post("http://stt:5001/stt", files = {"audio": open(sample_audios[0], "rb")})
    return response.text

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)