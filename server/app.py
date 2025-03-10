from flask import Flask, render_template, jsonify
import aiosqlite

app = Flask(__name__)

DATABASE = '../bot/database.db'


async def get_first_user():
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT user_id, username, balance FROM user LIMIT 1") as cursor:
            user = await cursor.fetchone()
            return user


async def get_all_posts():
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT task, description, link, bonus FROM post") as cursor:
            posts = await cursor.fetchall()
            return posts


async def update_user_balance(user_id, amount):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("UPDATE user SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
        await db.commit()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index1')
async def index1():
    user = await get_first_user()
    posts = await get_all_posts()

    if user:
        user_id, username, balance = user
        return render_template('index1.html', user_id=user_id, username=username, balance=balance, posts=posts)
    return "No user found"


@app.route('/add_bonus', methods=['POST'])
async def add_bonus():
    user = await get_first_user()
    if user:
        user_id = user[0]
        await update_user_balance(user_id, 10)
        return jsonify(success=True, message="Bonus added!")
    return jsonify(success=False, message="User not found.")


if __name__ == '__main__':
    app.run(debug=True)