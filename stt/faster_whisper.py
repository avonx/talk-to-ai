import requests
import time
import base64
import os

from dotenv import load_dotenv

load_dotenv()


class FasterWhisper:
    """
    faster_whisper on Runpod
    https://doc.runpod.io/reference/faster-whisper
    """

    def __init__(self):
        self.api_url = os.environ.get("FASTER_WHISPER_API_URL")
        self.api_key = os.environ.get("FASTER_WHISPER_API_KEY")
        self.laguage = os.environ.get("LANGUAGE")
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": self.api_key,
        }

    def transcribe(self, audio_data):
        start_time = time.time()
        audio_base64 = base64.b64encode(audio_data).decode("utf-8")
        payload = {
            "input": {
                "audio_base64": audio_base64,
                "model": "base",
                "transcription": "plain_text",
                "translate": False,
                "language": os.environ.get("LANGUAGE"),
                "temperature": 0,
                "best_of": 5,
                "beam_size": 5,
                "patience": 1,
                "suppress_tokens": "-1",
                "condition_on_previous_text": False,
                "temperature_increment_on_fallback": 0.2,
                "compression_ratio_threshold": 2.4,
                "logprob_threshold": -1,
                "no_speech_threshold": 0.6,
                "word_timestamps": False,
            },
            "enable_vad": False,
        }
        response = requests.post(self.api_url, json=payload, headers=self.headers)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"STT elapsed time: {elapsed_time:.2f} seconds")
        print("Faster-Whisper response:", response.json())
        return response.json()["output"]["transcription"]
