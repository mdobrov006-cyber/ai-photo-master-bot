import os

from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_message(chat_id, text, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }

    if reply_markup:
        payload["reply_markup"] = reply_markup

    requests.post(
        f"{TELEGRAM_API}/sendMessage",
        json=payload,
        timeout=10,
    )


def main_menu(chat_id):
    keyboard = {
        "inline_keyboard": [
            [{"text": "✨ О продукте", "callback_data": "product"}],
            [{"text": "💳 Купить AI PHOTO MASTER — 2 990 ₽", "callback_data": "buy"}],
            [
                {"text": "📄 Оферта", "callback_data": "offer"},
                {"text": "🔒 Конфиденциальность", "callback_data": "privacy"},
            ],
            [{"text": "💬 Поддержка", "callback_data": "support"}],
        ]
    }

    send_message(
        chat_id,
        "✨ <b>Добро пожаловать в AI Photo Master!</b>\n\n"
        "AI PHOTO MASTER — практическая инструкция по созданию "
        "реалистичных AI-фотографий с телефона.\n\n"
        "Выберите нужный раздел 👇",
        keyboard,
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
        main_menu(chat["id"])
        return "OK", 200

    callback = update.get("callback_query")

    if callback:
        chat_id = callback["message"]["chat"]["id"]
        data = callback.get("data")

        requests.post(
            f"{TELEGRAM_API}/answerCallbackQuery",
            json={"callback_query_id": callback["id"]},
            timeout=10,
        )

        if data == "product":
            send_message(
                chat_id,
                "✨ <b>AI PHOTO MASTER</b>\n\n"
                "Практическая пошаговая система, которая поможет создавать "
                "реалистичные AI-фотографии с телефона.\n\n"
                "Внутри:\n"
                "• подготовка исходного фото;\n"
                "• быстрый старт;\n"
                "• 25+ готовых промптов;\n"
                "• создание и расширение образов;\n"
                "• разбор ошибок;\n"
                "• мини-редактирование;\n"
                "• бонусный материал.\n\n"
                "Стоимость: <b>2 990 ₽</b>.\n"
                "Доступ к продукту предоставляется на 1 год.\n\n"
                "Использование сторонних AI-сервисов оплачивается отдельно "
                "по тарифам выбранного сервиса."
            )

        elif data == "buy":
            send_message(
                chat_id,
                "💳 <b>Оплата AI PHOTO MASTER — 2 990 ₽</b>\n\n"
                "Платёжный модуль сейчас подключается.\n"
                "После подключения Cashera здесь будет доступна кнопка оплаты.\n\n"
                "Это временная заглушка для прохождения проверки сервиса."
            )

        elif data == "offer":
            send_message(
                chat_id,
                "📄 <b>Публичная оферта</b>\n\n"
                "Продавец предлагает приобрести цифровой продукт "
                "AI PHOTO MASTER стоимостью 2 990 ₽.\n\n"
                "После успешной оплаты покупателю предоставляется доступ "
                "к цифровому продукту.\n\n"
                "Срок доступа — 1 год.\n\n"
                "AI PHOTO MASTER включает методические материалы, инструкции "
                "и промпты. Услуги сторонних AI-сервисов в стоимость продукта "
                "не входят и оплачиваются покупателем самостоятельно.\n\n"
                "Оформляя покупку, пользователь подтверждает согласие "
                "с условиями приобретения цифрового продукта."
            )

        elif data == "privacy":
            send_message(
                chat_id,
                "🔒 <b>Политика конфиденциальности</b>\n\n"
                "Персональные данные используются только в объёме, необходимом "
                "для обработки оплаты, предоставления доступа к продукту "
                "и связи с покупателем.\n\n"
                "Данные не передаются третьим лицам, кроме случаев, необходимых "
                "для обработки платежа или предусмотренных законодательством.\n\n"
                "Используя бот и оформляя покупку, пользователь соглашается "
                "с обработкой необходимых данных для исполнения заказа."
            )

        elif data == "support":
            keyboard = {
                "inline_keyboard": [
                    [
                        {
                            "text": "Написать в Instagram",
                            "url": "https://www.instagram.com/aiphotomasterr/",
                        }
                    ]
                ]
            }

            send_message(
                chat_id,
                "💬 <b>Поддержка AI PHOTO MASTER</b>\n\n"
                "По вопросам продукта и оплаты напишите нам в Direct Instagram:",
                keyboard,
            )

    return "OK", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
