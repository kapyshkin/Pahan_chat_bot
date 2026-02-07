import sqlite3
import os
import random
from aiogram import Bot, Dispatcher, executor, types

TOKEN = os.getenv("TOKEN")

# 🔥 ТВОЙ TELEGRAM ID
BOSS_ID = 6341558087

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

conn = sqlite3.connect("rating.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    points INTEGER
)
""")
conn.commit()

def get_rank(p):
    if p < 10: return "🤡 Чушпан"
    if p < 30: return "🪤 Терпила"
    if p < 60: return "🍺 Подпивас с мнением"
    if p < 100: return "🧱 Дворовой"
    if p < 150: return "😎 Авторитет"
    if p < 200: return "👀 Смотрящий"
    if p < 300: return "🐺 Смотряга"
    return "👑 Батя чата"

def get_user(u):
    cursor.execute("SELECT points FROM users WHERE user_id=?", (u.id,))
    r = cursor.fetchone()
    if not r:
        start = 300 if u.id == BOSS_ID else 0
        cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (u.id, u.username, start))
        conn.commit()
        return start
    return r[0]

@dp.message_handler(commands=["me"])
async def me(m: types.Message):
    p = 300 if m.from_user.id == BOSS_ID else get_user(m.from_user)
    await m.reply(
        f"👤 {m.from_user.first_name}\n"
        f"⭐ Очки: {p}\n"
        f"🏷 Звание: {get_rank(p)}"
    )

@dp.message_handler(commands=["rep"])
async def rep(m: types.Message):
    if not m.reply_to_message:
        return await m.reply("Ответь на сообщение 😈")

    t = m.reply_to_message.from_user
    if t.id == BOSS_ID:
        return await m.reply("❌ Батю трогать нельзя 👑")

    p = get_user(t) + 1
    cursor.execute("UPDATE users SET points=? WHERE user_id=?", (p, t.id))
    conn.commit()
    await m.reply(f"➕ @{t.username} → {get_rank(p)} ({p})")

@dp.message_handler(commands=["minus"])
async def minus(m: types.Message):
    if not m.reply_to_message:
        return await m.reply("Ответь на сообщение 😏")

    t = m.reply_to_message.from_user
    if t.id == BOSS_ID:
        return await m.reply("❌ Батя неприкасаем 👑")

    member = await bot.get_chat_member(m.chat.id, m.from_user.id)
    dmg = 5 if member.is_chat_admin() else 1

    p = get_user(t) - dmg
    if p < 0: p = 0
    cursor.execute("UPDATE users SET points=? WHERE user_id=?", (p, t.id))
    conn.commit()
    await m.reply(f"➖ @{t.username} наказан\n🏷 {get_rank(p)} ({p})")

@dp.message_handler(commands=["top"])
async def top(m: types.Message):
    cursor.execute("SELECT username, points FROM users ORDER BY points DESC LIMIT 10")
    rows = cursor.fetchall()

    text = "🏆 ТОП ЧАТА:\n"
    for i, (u, p) in enumerate(rows, 1):
        text += f"{i}. @{u} — {p} ({get_rank(p)})\n"

    await m.reply(text)

# 💀 КАЗНЬ ДНЯ — ТОЛЬКО БАТЯ
@dp.message_handler(commands=["kazn"])
async def kazn(m: types.Message):
    if m.from_user.id != BOSS_ID:
        return

    cursor.execute("SELECT user_id, username FROM users WHERE user_id != ?", (BOSS_ID,))
    users = cursor.fetchall()
    if not users:
        return await m.reply("Некого казнить 😈")

    victim_id, victim_name = random.choice(users)
    p = get_user(types.User(id=victim_id, username=victim_name)) - 5
    if p < 0: p = 0

    cursor.execute("UPDATE users SET points=? WHERE user_id=?", (p, victim_id))
    conn.commit()

    await m.reply(f"💀 КАЗНЬ ДНЯ\n@{victim_name} получает −5\n🏷 {get_rank(p)} ({p})")

if __name__ == "__main__":
    executor.start_polling(dp)
