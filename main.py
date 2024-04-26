from flask import Flask, render_template, request, Response
import os
import logging
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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/", methods=["GET"])
def index():
    logger.info("Received GET request for /")
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    logger.info("Received POST request for /chat")
    audio_data = request.files["audio"].read()

    # STT
    user_message = stt.transcribe(audio_data)
    logger.info(f"User message: {user_message}")

    # LLM
    bot_message = llm.generate_response(user_message)
    logger.info(f"Bot message: {bot_message}")

    # TTS
    audio_data = tts.synthesize(bot_message)

    # When TTS is streaming model
    if hasattr(audio_data, "__iter__"):
        return Response(audio_data, mimetype="audio/mpeg")
    else:
        return Response(audio_data, mimetype="audio/mpeg")

def main(request):
    if request.method == 'GET':
        logger.info("Dispatching GET request to index()")
        return index()
    elif request.method == 'POST':
        logger.info("Dispatching POST request to chat()")
        return chat()

if __name__ == "__main__":
    app.run()