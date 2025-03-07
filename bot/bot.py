import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
# from aiogram.utils import executor
import stripe
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
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton('Оплата'))
keyboard.add(KeyboardButton('Проверка оплаты'))

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот для оплаты через Stripe.", reply_markup=keyboard)

# Обработчик кнопки "Оплата"
@dp.message_handler(lambda message: message.text == 'Оплата')
async def process_payment(message: types.Message):
    # Создаем платежное намерение (Payment Intent) в Stripe
    payment_intent = stripe.PaymentIntent.create(
        amount=1000,  # Сумма в центах (10.00 USD)
        currency='usd',
        payment_method_types=['card'],
    )

    # Отправляем клиенту ссылку на оплату
    await message.reply(f"Оплатите 10.00 USD: {payment_intent['client_secret']}")

# Обработчик кнопки "Проверка оплаты"
@dp.message_handler(lambda message: message.text == 'Проверка оплаты')
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
