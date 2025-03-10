import sqlite3
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = '8165391157:AAHJr_b-FRzZUwM5S_FTM4WLqXUqThYij_k'
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# Подключение к базе данных
conn = sqlite3.connect("referrals.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        referrer_id INTEGER,
        points INTEGER DEFAULT 0
    )
""")
conn.commit()


def add_user(user_id, username, referrer_id=None):
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (user_id, username, referrer_id, points) VALUES (?, ?, ?, 0)",
                       (user_id, username, referrer_id))
        conn.commit()
        if referrer_id:
            update_points(referrer_id, 3)
            notify_referrer(referrer_id, username, 3)
            cursor.execute("SELECT referrer_id FROM users WHERE user_id = ?", (referrer_id,))
            second_level_ref = cursor.fetchone()
            if second_level_ref and second_level_ref[0]:
                update_points(second_level_ref[0], 1)
                notify_referrer(second_level_ref[0], username, 1)


def update_points(user_id, points):
    cursor.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (points, user_id))
    conn.commit()


def get_points(user_id):
    cursor.execute("SELECT points FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else 0


def notify_referrer(referrer_id, new_username, points):
    asyncio.create_task(bot.send_message(referrer_id, f"Ваш реферал @{new_username} принес вам {points} баллов!"))


def get_referrals(user_id):
    cursor.execute("SELECT username FROM users WHERE referrer_id = ?", (user_id,))
    referrals = cursor.fetchall()
    return [ref[0] for ref in referrals]


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or f"user_{user_id}"
    referrer_id = None
    if len(message.text.split()) > 1:
        referrer_id = int(message.text.split()[1])
        if referrer_id == user_id:
            referrer_id = None
    add_user(user_id, username, referrer_id)

    referral_link = f"https://t.me/HistoBit_bot?start={user_id}"
    message_text = f"Привет, {message.from_user.first_name}!\nТвои баллы: {get_points(user_id)}\n\nПриглашай друзей по этой ссылке и зарабатывай баллы:\n {referral_link}"
    await message.answer(message_text)


@dp.message_handler(commands=['points'])
async def show_points(message: types.Message):
    user_id = message.from_user.id
    await message.answer(f"У тебя {get_points(user_id)} баллов.")


@dp.message_handler(commands=['ref'])
async def show_referrals(message: types.Message):
    user_id = message.from_user.id
    referrals = get_referrals(user_id)
    if referrals:
        referral_list = "\n".join([f"@{r}" for r in referrals])
        await message.answer(f"Твои рефералы:\n{referral_list}")
    else:
        await message.answer("У тебя пока нет рефералов.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
