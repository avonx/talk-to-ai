from .bertvits2 import BertVits2
from .elevenlabs import ElevenLabs
from .azure import AzureTTS
from .elevenlabs_streaming import ElevenLabsStreaming


class TextToSpeech:
    def __init__(self, tts_type, config, character_config):
        if tts_type == "bertvits2":
            self.tts = BertVits2(config, character_config)
        elif tts_type == "elevenlabs":
            self.tts = ElevenLabs(config, character_config)
        elif tts_type == "azure":
            self.tts = AzureTTS(config, character_config)
        elif tts_type == "elevenlabs_streaming":
            self.tts = ElevenLabsStreaming(config, character_config)
        else:
            raise ValueError(f"Unsupported TTS type: {tts_type}")

    def synthesize(self, text):
        return self.tts.synthesize(text)
