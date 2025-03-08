from flask import Flask, request, jsonify
import stripe
from config import *
from aiogram import Bot
import logging
import json
import asyncio

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Ваш секретный ключ Stripe
#STRIPE_SECRET_KEY = 'YOUR_STRIPE_SECRET_KEY'
stripe.api_key = STRIPE_SECRET_KEY



# Инициализация бота
# BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = Bot(token=BOT_TOKEN)

#Асинхронная функция для отправки сообщения
async def send_telegram_message(user_id, text):
    await bot.send_message(user_id, text)

# Синхронная обертка для запуска асинхронной функции
def send_message_sync(user_id, text):
    asyncio.run(send_telegram_message(user_id, text))

# Эндпоинт для вебхука
@app.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        logging.error("Error")
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        logging.error("Error")
        raise e

    # # Обработка события
    # if event['type'] == 'payment_intent.succeeded':
    #     payment_intent = event['data']['object']
    #     # Логика обработки успешной оплаты
    #     print(f"Payment succeeded: {payment_intent['id']}")

    # Логирование всего события
    logging.info("EVENT: %s", json.dumps(event, indent=2))

    # Обработка события
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session.get('client_reference_id')  # Получаем user_id
        logging.info(f"Оплата прошла user_id {user_id}")

        if user_id:
            # Отправляем сообщение пользователю в Telegram
            bot.send_message(user_id, "Оплата прошла успешно! Спасибо за покупку.")

    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4242)
