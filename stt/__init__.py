from .whisper import Whisper
from .faster_whisper import FasterWhisper


class SpeechToText:
    def __init__(self, stt_type):
        if stt_type == "whisper":
            self.stt = Whisper()
        elif stt_type == "faster_whisper":
            self.stt = FasterWhisper()
        else:
            raise ValueError(f"Unsupported STT type: {stt_type}")

    def transcribe(self, audio_data):
        return self.stt.transcribe(audio_data)
