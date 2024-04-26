import yaml
from flask import Flask, render_template, request, Response, session, make_response
import os
import uuid
import logging
from stt import SpeechToText
from llm import LanguageModel
from tts import TextToSpeech

app = Flask(__name__)
app.secret_key = "your_secret_key_6"  # セッションを使用するために秘密鍵を設定

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# インスタンスを管理するための辞書
instances = {}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/", methods=["GET"])
def index():
    characters = config["characters"]
    user_id = request.cookies.get("user_id")
    if not user_id:
        user_id = str(uuid.uuid4())
        session["user_id"] = user_id
        response = make_response(render_template("index.html", characters=characters))
        response.set_cookie("user_id", user_id)
        return response
    else:
        session["user_id"] = user_id
        return render_template("index.html", characters=characters)


@app.route("/chat", methods=["POST"])
def chat():
    character_name = request.form["character_name"]
    user_id = session["user_id"]

    if (
        user_id not in instances
        or instances[user_id]["character_name"] != character_name
    ):
        # キャラクターが変更された場合、新しいインスタンスを作成
        character_config = config["characters"][character_name]
        instances[user_id] = {
            "character_name": character_name,
            "stt": SpeechToText(
                character_config["stt"],
                config["stt"][character_config["stt"]],
                character_config,
            ),
            "llm": LanguageModel(
                character_config["llm"],
                config["llm"][character_config["llm"]],
                character_config,
            ),
            "tts": TextToSpeech(
                character_config["tts"],
                config["tts"][character_config["tts"]],
                character_config,
            ),
        }
    # ユーザーIDを使用してインスタンスを取得
    stt = instances[user_id]["stt"]
    llm = instances[user_id]["llm"]
    tts = instances[user_id]["tts"]

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
    if request.method == "GET":
        logger.info("Dispatching GET request to index()")
        return index()
    elif request.method == "POST":
        logger.info("Dispatching POST request to chat()")
        return chat()


if __name__ == "__main__":
    app.run()
