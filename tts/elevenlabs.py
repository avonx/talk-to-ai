import requests
import os
import time

from dotenv import load_dotenv

load_dotenv()


class ElevenLabs:
    def __init__(self):
        self.api_url = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        self.api_key = os.environ.get("ELEVENLABS_API_KEY")
        self.voice_id = os.environ.get("ELEVENLABS_VOICE_ID")
        self.headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key,
        }

    def synthesize(self, text):
        start_time = time.time()
        data = {
            "text": text,
            "model_id": os.environ.get("ELEVENLABS_MODEL_ID"),
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
        }
        response = requests.post(
            self.api_url.format(voice_id=self.voice_id), json=data, headers=self.headers
        )

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"TTS elapsed time: {elapsed_time:.2f} seconds")

        return response.content
