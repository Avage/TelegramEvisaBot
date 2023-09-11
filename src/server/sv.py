from flask import Flask, request
import telebot
from src.crypto import payment


def create_app(bot):
    app = Flask(__name__)

    @app.route('/', methods=['POST'])
    def webhook():
        update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
        bot.process_new_updates([update])
        return {"ok": True}

    @app.route('/tgwallet/ipn', methods=['POST'])
    def wallet():
        temp = payment.is_valid(request)
        for event in request.get_json():
            if event["type"] == "ORDER_PAID" and temp:
                bot.process_new_updates([telebot.types.Update.de_json(event)])
        return 'OK'

    app.run()
