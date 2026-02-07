from aiogram import Bot, Dispatcher, executor, types

TOKEN = "8521920418:AAH8IMVKq62_sajLQCZlkHg2dpWRguSSVe8"
PAHAN_ID = 6341558087

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

ratings = {}

def get_rank(points):
    if points < 10:
        return "🤡 Чушпан"
    elif points < 30:
        return "🪤 Терпила"
    elif points < 60:
        return "🍺 Подпивас"
    elif points < 100:
        return "🧱 Дворовой"
    elif points < 150:
        return "😎 Авторитет"
    elif points < 200:
        return "👀 Смотрящий"
    elif points < 300:
        return "🐺 Смотряга"
    else:
        return "👑 Батя чата"

@dp.message_handler(commands=["plus"])
async def plus(msg: types.Message):
    uid = msg.reply_to_message.from_user.id
    ratings[uid] = ratings.get(uid, 0) + 1
    await msg.reply("➕ Засчитано")

@dp.message_handler(commands=["me"])
async def me(msg: types.Message):
    uid = msg.from_user.id
    pts = ratings.get(uid, 0)
    rank = "👑 Пахан чата" if uid == PAHAN_ID else get_rank(pts)
    await msg.reply(f"Твой статус: {rank}\nОчки: {pts}")

@dp.message_handler(commands=["kazn"])
async def kazn(msg: types.Message):
    if msg.from_user.id == PAHAN_ID:
        await msg.reply("☠️ Казнь дня исполнена. Батя решил.")
    else:
        await msg.reply("❌ Не твоего уровня команда")

if __name__ == "__main__":
    executor.start_polling(dp)
