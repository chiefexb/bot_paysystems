import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode
import stripe

# from aiogram.utils import executor

from config import *

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
# API_TOKEN = BOT_TOKEN
#STRIPE_SECRET_KEY = 'YOUR_STRIPE_SECRET_KEY'

# bot = Bot(token=BOT_TOKEN)
# dp = Dispatcher(bot)
#parse_mode=ParseMode.HTML
bot = Bot(token=BOT_TOKEN)  # Указываем parse_mode
dp = Dispatcher()  # Создаем Dispatcher без аргументо


# Инициализация Stripe
stripe.api_key = STRIPE_SECRET_KEY

# Создание клавиатуры с кнопками
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Оплата')],
        [KeyboardButton(text='Проверка оплаты')]
    ],
    resize_keyboard=True
)

# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот для оплаты через Stripe.", reply_markup=keyboard)


@dp.message(lambda message: message.text == 'Оплата')
async def process_payment(message: types.Message):
    # Создаем Payment Intent в Stripe
    payment_intent = stripe.PaymentIntent.create(
        amount=1000,  # Сумма в центах (10.00 USD)
        currency='usd',
        payment_method_types=['card'],
        metadata={
            'user_id': message.from_user.id  # Сохраняем ID пользователя
        },
    )

    # Создаем сессию Stripe Checkout
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Тестовый платеж',
                },
                'unit_amount': 1000,  # 10.00 USD
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=f'{SITE_URL}/success',  # URL после успешной оплаты
        cancel_url=f'{SITE_URL}/cancel',    # URL после отмены
    )

    # Отправляем пользователю ссылку на оплату
    await message.reply(f"Оплатите 10.00 USD: {checkout_session.url}")
# Обработчик кнопки "Оплата"
# @dp.message(lambda message: message.text == 'Оплата')
# async def process_payment(message: types.Message):
#     # Создаем платежное намерение (Payment Intent) в Stripe
#     payment_intent = stripe.PaymentIntent.create(
#         amount=1000,  # Сумма в центах (10.00 USD)
#         currency='usd',
#         payment_method_types=['card'],
#     )
#
#     # Отправляем клиенту ссылку на оплату
#     await message.reply(f"Оплатите 10.00 USD: {payment_intent['client_secret']}")

# Обработчик кнопки "Проверка оплаты"
@dp.message(lambda message: message.text == 'Проверка оплаты')
async def check_payment(message: types.Message):
    # Здесь можно реализовать логику проверки оплаты
    # Например, запрос к Stripe API для проверки статуса платежа
    await message.reply("Проверка оплаты...")


# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
