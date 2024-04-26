import requests
import os
import time


class ElevenLabs:
    def __init__(self, config, character_config):
        self.api_key = config["elevenlabs_api_key"]
        self.voice_id = character_config["tts-id"]
        self.elevenlabs_model_id = config["elevenlabs_model_id"]
        self.headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key,
        }

    def synthesize(self, text):
        start_time = time.time()
        data = {
            "text": text,
            "model_id": self.elevenlabs_model_id,
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
        }
        response = requests.post(
            self.api_url.format(voice_id=self.voice_id), json=data, headers=self.headers
        )

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"TTS elapsed time: {elapsed_time:.2f} seconds")

        return response.content
