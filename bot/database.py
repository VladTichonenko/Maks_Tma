# database.py
import aiosqlite

async def create_db():
    async with aiosqlite.connect('database.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS user (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                balance REAL DEFAULT 0,
                referal INTEGER,
                referaltwo INTEGER
            )
        ''')

        await db.execute('''
            CREATE TABLE IF NOT EXISTS post (
                task TEXT,
                description TEXT,
                link TEXT,
                bonus INTEGER
            )
        ''')

        # Создание таблицы chat
        await db.execute('''
            CREATE TABLE IF NOT EXISTS chat (
                admin TEXT,
                user_id INTEGER,
                otvet TEXT,
                vopros TEXT,
                FOREIGN KEY(user_id) REFERENCES user(user_id)
            )
        ''')

        await db.commit()

async def add_user(user_id, username, referal=None, referaltwo=None):
    async with aiosqlite.connect('database.db') as db:
        cursor = await db.execute('SELECT user_id FROM user WHERE user_id = ?', (user_id,))
        existing_user = await cursor.fetchone()

        if existing_user is None:
            await db.execute('''
                INSERT INTO user (user_id, username, balance, referal, referaltwo) VALUES (?, ?, ?, ?, ?)
            ''', (user_id, username, 0, referal, referaltwo))  # Баланс по умолчанию 0
            await db.commit()

async def add_post(task, description, link, bonus):
    async with aiosqlite.connect('database.db') as db:
        await db.execute('''
            INSERT INTO post (task, description, link, bonus) VALUES (?, ?, ?, ?)
        ''', (task, description, link, bonus))
        await db.commit()

async def update_user_balance(user_id, amount):
    async with aiosqlite.connect('database.db') as db:
        await db.execute('UPDATE user SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
        await db.commit()

async def get_user_by_id(user_id):
    async with aiosqlite.connect('database.db') as db:
        cursor = await db.execute('SELECT * FROM user WHERE user_id = ?', (user_id,))
        return await cursor.fetchone()

async def add_chat_entry(admin, user_id, vopros, otvet):
    async with aiosqlite.connect('database.db') as db:
        await db.execute('''
            INSERT INTO chat (admin, user_id, vopros, otvet) VALUES (?, ?, ?, ?)
        ''', (admin, user_id, vopros, otvet))
        await db.commit()

async def get_chat_history(user_id):
    async with aiosqlite.connect('database.db') as db:
        cursor = await db.execute('SELECT vopros, otvet FROM chat WHERE user_id = ? ORDER BY rowid', (user_id,))
        return await cursor.fetchall()