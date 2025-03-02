import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database import create_db, add_user, update_user_balance, get_user_by_id, add_post, get_chat_history

API_TOKEN = '8165391157:AAHJr_b-FRzZUwM5S_FTM4WLqXUqThYij_k'
ADMIN_ID = 6850731097  # Замените на ваш ID

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def on_startup(dp):
    await create_db()  # Создание базы данных при старте бота


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username

    referral_id = message.get_args()

    if await add_user(user_id, username, referral_id):
        if referral_id:
            referrer = await get_user_by_id(referral_id)
            if referrer:
                await update_user_balance(referral_id, 5)
                await bot.send_message(referral_id, f"🎉 {username} стал вашим рефералом! Вы получили 5 баллов.")

        await message.reply("Добро пожаловать! Вы успешно зарегистрированы.")
    else:
        await message.reply("Вы уже зарегистрированы.")


@dp.message_handler(commands=['admin'])
async def admin_panel(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton("Добавить пост", callback_data="add_post"),
            InlineKeyboardButton("Ответить на вопросы", callback_data="reply_questions")
        )
        await message.reply("Админ-панель. Выберите действие:", reply_markup=keyboard)
    else:
        await message.reply("У вас нет прав доступа к админ-панели.")


@dp.callback_query_handler(text="add_post")
async def add_post_command(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           "Введите данные для нового поста в формате:\n/task <task>\n/description <description>\n/link <link>\n/bonus <bonus>")


@dp.callback_query_handler(text="reply_questions")
async def reply_questions(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    # Получаем все вопросы из базы данных
    user_id = callback_query.from_user.id
    questions = await get_chat_history(user_id)

    if not questions:
        await bot.send_message(user_id, "Нет вопросов для ответа.")
        return

    for question in questions:
        vopros, _ = question
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("Ответить", callback_data=f"reply_{vopros}")
        )
        await bot.send_message(user_id, f"Вопрос: {vopros}", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data.startswith('reply_'))
async def process_reply(callback_query: types.CallbackQuery):
    question = callback_query.data[6:]  # Получаем текст вопроса
    await bot.answer_callback_query(callback_query.id)

    await bot.send_message(callback_query.from_user.id, f"Введите ответ на вопрос: {question}")
    await dp.current_state(user=callback_query.from_user.id).update_data(current_question=question)
    await dp.current_state(user=callback_query.from_user.id).set_state("waiting_for_reply")


@dp.message_handler(state="waiting_for_reply")
async def handle_reply(message: types.Message):
    data = await dp.current_state(user=message.from_user.id).get_data()
    question = data.get("current_question")

    if question:
        # Сохраняем ответ в базу данных
        await add_post("Ответ на вопрос", message.text, "", 0)  # Здесь можно добавить логику для сохранения ответа
        await message.reply("Ответ успешно сохранен!")
        await dp.current_state(user=message.from_user.id).reset_data()
    else:
        await message.reply("Ошибка: Неизвестный вопрос.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)