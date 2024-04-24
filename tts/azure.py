import requests
import time
import os
from xml.etree import ElementTree

from dotenv import load_dotenv

load_dotenv()


class AzureTTS:
    def __init__(self):
        self.subscription_key = os.environ.get("AZURE_SPEECH_KEY")
        self.region = os.environ.get("AZURE_SPEECH_REGION")
        self.language = os.environ.get("AZURE_SPEECH_LANGUAGE")
        self.voice_name = os.environ.get("AZURE_SPEECH_VOICE_NAME")
        self.output_format = os.environ.get(
            "AZURE_SPEECH_OUTPUT_FORMAT", "riff-24khz-16bit-mono-pcm"
        )
        self.session = requests.Session()
        self.connect()

    def connect(self):
        url = f"https://{self.region}.tts.speech.microsoft.com/cognitiveservices/v1"
        headers = {
            "Ocp-Apim-Subscription-Key": self.subscription_key,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": self.output_format,
        }
        self.session.headers.update(headers)
        self.session.post(url)

    def synthesize(self, text):
        start_time = time.time()

        url = f"https://{self.region}.tts.speech.microsoft.com/cognitiveservices/v1"

        xml_body = ElementTree.Element("speak", version="1.0")
        xml_body.set("{http://www.w3.org/XML/1998/namespace}lang", "en-US")
        voice = ElementTree.SubElement(xml_body, "voice")
        voice.set("{http://www.w3.org/XML/1998/namespace}lang", self.language)
        voice.set("name", self.voice_name)
        voice.text = text
        body = ElementTree.tostring(xml_body)

        response = self.session.post(url, data=body, stream=True)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"TTS elapsed time: {elapsed_time:.2f} seconds")

        if response.status_code == 200:
            return response.iter_content(chunk_size=1024)
        else:
            print(
                f"Failed to synthesize speech: {response.status_code} - {response.reason}"
            )
            return None
