import requests
import os
import time


class Whisper:
    def __init__(self, config, character_config):
        self.api_url = config["whisper_api_url"]
        self.api_key = config["openai_api_key"]
        self.language = character_config["language"]

    def transcribe(self, audio_data):
        start_time = time.time()
        files = {"file": ("audio.wav", audio_data)}
        response = requests.post(
            self.api_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            files=files,
            data={
                "model": "whisper-1",
                "language": self.language,
            },
        )
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"STT elapsed time: {elapsed_time:.2f} seconds")
        return response.json()["text"]
