import discord
from discord.ext import commands
import os
import random
import unicodedata
from collections import defaultdict
import asyncio

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ========================
# CẤU HÌNH
# ========================

toxic_words = ["ngu", "mkid", "oc cho", "do dien", "clan tao"]
toxic_count = defaultdict(int)

responses = [
    "😏 Emoji cũng không thoát đâu nha",
    "🚨 Nói chuyện lịch sự đi bạn",
    "🤨 Gắt vậy ai chơi?",
    "🧠 Bình tĩnh nào bro"
]

MUTE_DURATION = 60  # giây
MAX_WARN = 3

# ========================
# HÀM CHUẨN HOÁ TEXT
# ========================

def normalize_text(text):
    # Chuyển regional indicator 🇦 🇧 🇨 -> abc
    new_text = ""
    for char in text:
        if 0x1F1E6 <= ord(char) <= 0x1F1FF:
            new_text += chr(ord(char) - 0x1F1E6 + ord('a'))
        else:
            new_text += char

    # Bỏ dấu tiếng Việt
    new_text = unicodedata.normalize('NFD', new_text)
    new_text = ''.join(c for c in new_text if unicodedata.category(c) != 'Mn')

    return new_text.lower()

# ========================
# EVENT
# ========================

@bot.event
async def on_ready():
    print(f"🔥 Whaley online: {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓")

@bot.command()
async def toxic(ctx):
    count = toxic_count[ctx.author.id]
    await ctx.send(f"⚠ Bạn đã toxic {count} lần.")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = normalize_text(message.content)

    if any(word in content for word in toxic_words):

        toxic_count[message.author.id] += 1

        # Xoá tin nhắn toxic
        try:
            await message.delete()
        except:
            pass

        await message.channel.send(
            f"{message.author.mention} {random.choice(responses)}"
        )

        # Nếu vượt quá giới hạn -> mute
        if toxic_count[message.author.id] >= MAX_WARN:
            role = discord.utils.get(message.guild.roles, name="Muted")

            if not role:
                role = await message.guild.create_role(name="Muted")
                for channel in message.guild.channels:
                    await channel.set_permissions(role, send_messages=False)

            await message.author.add_roles(role)

            await message.channel.send(
                f"🔇 {message.author.mention} bị mute {MUTE_DURATION} giây vì toxic quá nhiều!"
            )

            await asyncio.sleep(MUTE_DURATION)

            await message.author.remove_roles(role)
            toxic_count[message.author.id] = 0

    await bot.process_commands(message)

bot.run(TOKEN)
