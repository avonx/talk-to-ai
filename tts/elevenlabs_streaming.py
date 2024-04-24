import os
import requests
from typing import Iterator
import time

from dotenv import load_dotenv

load_dotenv()


class ElevenLabsStreaming:
    def __init__(self):
        self.api_key = os.environ.get("ELEVENLABS_API_KEY")
        self.voice_id = os.environ.get("ELEVENLABS_VOICE_ID")
        self.api_url = (
            f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}/stream"
        )
        self.optimize_streaming_latency = int(
            os.environ.get("ELEVENLABS_OPTIMIZE_STREAMING_LATENCY", 0)
        )

    def synthesize(self, text: str) -> Iterator[bytes]:
        start_time = time.time()
        headers = {
            "Accept": "audio/mpeg",
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
        }

        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5,
            },
            "optimize_streaming_latency": self.optimize_streaming_latency,
        }

        with requests.post(
            self.api_url, headers=headers, json=data, stream=True
        ) as response:
            if response.status_code == 200:
                for i, chunk in enumerate(response.iter_content(chunk_size=1024)):
                    if chunk:
                        if i == 0:
                            elapsed_time = time.time() - start_time
                            print(f"Time until first chunk: {elapsed_time:.2f} seconds")
                        yield chunk
            else:
                print(
                    f"Failed to synthesize speech: {response.status_code} - {response.text}"
                )
                return None
