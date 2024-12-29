from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import asyncio
import os

API_TOKEN = os.getenv('BOT_TOKEN')  # Получение токена из переменной окружения
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Словарь для хранения результатов
scores = {}

@dp.message_handler(commands=['start'])
async def start_game(message: types.Message):
    scores.clear()  # Очистить результаты перед новой игрой
    await message.answer("Добро пожаловать! Кто первый реагирует, получает баллы. Напишите /play для начала игры.")

@dp.message_handler(commands=['play'])
async def play_round(message: types.Message):
    scores = {}
    task = "Нажмите на кнопку 'Есть ответ!'"
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Есть ответ!", callback_data="react")
    keyboard.add(button)
    await message.answer(task, reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == 'react')
async def reaction_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.full_name
    if len(scores) == 0:
        scores[user_id] = 1
        chat_id = callback_query.message.chat.id
        await bot.send_message(chat_id, f"{user_name}, вы были первым!")
    else:
        await bot.answer_callback_query(callback_query.id, text="Уже поздно!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

