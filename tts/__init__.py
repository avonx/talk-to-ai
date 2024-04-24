from .bertvits2 import BertVits2
from .elevenlabs import ElevenLabs
from .azure import AzureTTS
from .elevenlabs_streaming import ElevenLabsStreaming

class TextToSpeech:
    def __init__(self, tts_type):
        if tts_type == "bertvits2":
            self.tts = BertVits2()
        elif tts_type == "elevenlabs":
            self.tts = ElevenLabs()
        elif tts_type == "azure":
            self.tts = AzureTTS()
        elif tts_type == "elevenlabs_streaming":
            self.tts = ElevenLabsStreaming()
        else:
            raise ValueError(f"Unsupported TTS type: {tts_type}")
    
    def synthesize(self, text):
        return self.tts.synthesize(text)