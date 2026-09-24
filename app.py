import os

from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_message(chat_id, text):
    requests.post(
        f"{TELEGRAM_API}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text,
        },
        timeout=10,
    )


@app.route("/", methods=["GET"])
def home():
    return "AI Photo Master Bot is running", 200


@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    update = request.get_json(silent=True) or {}

    message = update.get("message", {})
    chat = message.get("chat", {})
    text = message.get("text", "")

    if text.startswith("/start") and chat.get("id"):
        send_message(
            chat["id"],
            "✨ Добро пожаловать в AI Photo Master!\n\n"
            "Здесь ты сможешь получить AI PHOTO MASTER "
            "и начать создавать свои реалистичные AI-образы."
        )

    return "OK", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
