from flask import Flask, request, jsonify
import stripe
from config import *

app = Flask(__name__)

# Ваш секретный ключ Stripe
#STRIPE_SECRET_KEY = 'YOUR_STRIPE_SECRET_KEY'
stripe.api_key = STRIPE_SECRET_KEY



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
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Обработка события
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        # Логика обработки успешной оплаты
        print(f"Payment succeeded: {payment_intent['id']}")

    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4242)
