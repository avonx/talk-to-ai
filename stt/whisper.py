import requests
import os
import time

from dotenv import load_dotenv

load_dotenv()


class Whisper:
    def __init__(self):
        self.api_url = os.environ.get("WHISPER_API_URL")

    def transcribe(self, audio_data):
        start_time = time.time()
        files = {"file": ("audio.wav", audio_data)}
        response = requests.post(
            self.api_url,
            headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
            files=files,
            data={
                "model": "whisper-1",
                "language": os.environ.get("LANGUAGE"),
            },
        )
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"STT elapsed time: {elapsed_time:.2f} seconds")
        return response.json()["text"]
