from flask import Flask, render_template, request, Response
import os
from stt import SpeechToText
from llm import LanguageModel
from tts import TextToSpeech

app = Flask(__name__)

# load .env
from dotenv import load_dotenv

load_dotenv()

# Initialize STT, LLM, TTS
stt = SpeechToText("whisper")
llm = LanguageModel("groq")
tts = TextToSpeech("elevenlabs_streaming")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    audio_data = request.files["audio"].read()

    # STT
    user_message = stt.transcribe(audio_data)
    print("User message:", user_message)

    # LLM
    bot_message = llm.generate_response(user_message)
    print("Bot message:", bot_message)

    # TTS
    audio_data = tts.synthesize(bot_message)

    # When TTS is streaming model
    if hasattr(audio_data, "__iter__"):
        return Response(audio_data, mimetype="audio/x-wav")
    else:
        return Response(audio_data, mimetype="audio/x-wav")


if __name__ == "__main__":
    app.run()
