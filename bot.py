from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import asyncio
import os

API_TOKEN = os.getenv('BOT_TOKEN')  # Получение токена из переменной окружения
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Создание кастомной клавиатуры для администратора
admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
admin_keyboard.add(KeyboardButton("Начать игру"))

# Словарь для хранения результатов
scores = {}

# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    # Проверяем, является ли пользователь администратором
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.is_chat_admin():
        # Если администратор, отправляем клавиатуру с кнопкой
        await message.reply("Привет, администратор! Вот меню управления:", reply_markup=admin_keyboard)
    else:
        # Если не администратор, отправляем обычное сообщение
        await message.reply("Добро пожаловать! У вас нет прав администратора.")

# Обработчик кнопки "Начать игру"
@dp.message_handler(lambda message: message.text == "Начать игру")
async def start_game_handler(message: types.Message):
    # Проверяем, является ли пользователь администратором
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.is_chat_admin():
        # Логика запуска игры
        scores.clear()
        task = "Нажмите на кнопку 'Есть ответ!'"
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Есть ответ!", callback_data="react")
        keyboard.add(button)
        await message.answer(task, reply_markup=keyboard)
    else:
        # Если не администратор, игнорируем
        await message.reply("Вы не администратор и не можете начинать игру.")

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

