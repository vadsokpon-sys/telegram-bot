import os
from flask import Flask, request
import requests

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

def send(chat_id, text):
    requests.post(URL + "/sendMessage", data={"chat_id": chat_id, "text": text})

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            send(chat_id, "Напиши сколько часов ты сидишь в соцсетях")
        else:
            try:
                h = float(text)

                if h <= 2:
                    level = "низкий"
                elif h <= 4:
                    level = "умеренный"
                elif h <= 6:
                    level = "высокий"
                else:
                    level = "чрезмерный"

                send(chat_id,
                     f"📊 Уровень: {level}\n"
                     f"🪞 Примерно {round(h/2,1)} фильма\n"
                     f"🌿 Попробуй меньше скроллить")

            except:
                send(chat_id, "Напиши число, например 5")

    return "ok"

@app.route("/", methods=["GET"])
def home():
    return "bot running"
