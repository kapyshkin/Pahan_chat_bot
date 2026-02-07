import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

PAHAN_ID = 6341558087 

@bot.event
async def on_ready():
    print(f'Запущен как {bot.user}')

@bot.command()
async def пахан(ctx):
    if ctx.author.id == PAHAN_ID:
        await ctx.send("👑 Пахан на месте. Всем тихо.")
    else:
        await ctx.send("❌ Ты не пахан.")

@bot.command()
async def казнь(ctx, member: discord.Member):
    if ctx.author.id == PAHAN_ID:
        await ctx.send(f"💀 {member.mention} — казнь исполнена. Батя решил.")
    else:
        await ctx.send("❌ Не твоего ума дело.")

bot.run("8521920418:AAH8IMVKq62_sajLQCZlkHg2dpWRguSSVe8")
