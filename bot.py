from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import asyncio

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
    task = "Нажмите на кнопку 'Быстрее!'"
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Быстрее!", callback_data="react")
    keyboard.add(button)
    await message.answer(task, reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == 'react')
async def reaction_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.full_name
    if user_id not in scores:
        scores[user_id] = 1
        await bot.answer_callback_query(callback_query.id, text=f"{user_name}, вы были первым!")
    else:
        await bot.answer_callback_query(callback_query.id, text="Уже поздно!")

@dp.message_handler(commands=['scores'])
async def show_scores(message: types.Message):
    if not scores:
        await message.answer("Пока никто не набрал очков.")
        return
    leaderboard = "\n".join([f"{message.chat.get_member(uid).user.full_name}: {score}" for uid, score in scores.items()])
    await message.answer(f"Результаты игры:\n{leaderboard}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

