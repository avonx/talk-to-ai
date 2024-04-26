import requests
import time
import base64
import os


class FasterWhisper:
    """
    faster_whisper on Runpod
    https://doc.runpod.io/reference/faster-whisper
    """

    def __init__(self, config, character_config):
        self.api_url = config["faster_whisper_api_url"]
        self.api_key = config["faster_api_key"]
        self.language = character_config["language"]

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
                "language": self.language,
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
