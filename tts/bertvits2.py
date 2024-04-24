import requests
import time
import os

from dotenv import load_dotenv

load_dotenv()


class BertVits2:
    def __init__(self):
        self.api_url = os.environ.get("BERTVITS2_API_URL")
        self.params = os.environ.get("BERTVITS2_PARAMS")
        self.params = eval(self.params)

    def synthesize(self, text):
        start_time = time.time()
        # self.paramsに text と speaker_name を追加
        self.params["text"] = text
        response = requests.get(self.api_url, params=self.params)
        # print(response.content)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"TTS elapsed time: {elapsed_time:.2f} seconds")
        return response.content
