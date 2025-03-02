# app.py
from flask import Flask, render_template, request, jsonify
import aiosqlite
import asyncio

app = Flask(__name__)

DATABASE = '../bot/database.db'


async def get_chat_history(user_id):
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute('SELECT vopros, otvet FROM chat WHERE user_id = ? ORDER BY rowid', (user_id,))
        return await cursor.fetchall()


@app.route('/')
def index():
    return render_template('chat.html')


@app.route('/chat/<int:user_id>', methods=['GET'])
async def chat(user_id):
    history = await get_chat_history(user_id)
    return jsonify(history)


@app.route('/send', methods=['POST'])
async def send():
    data = request.json
    admin = data['admin']
    user_id = data['user_id']
    question = data['question']
    answer = data['answer']

    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('INSERT INTO chat (admin, user_id, otvet, vopros) VALUES (?, ?, ?, ?)',
                         (admin, user_id, answer, question))
        await db.commit()

    return jsonify({'status': 'success'})


if __name__ == '__main__':
    asyncio.run(app.run(debug=True))