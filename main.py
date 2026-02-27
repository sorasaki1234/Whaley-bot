import discord
from discord.ext import commands
import os
import random
import unicodedata
from collections import defaultdict
import asyncio

# ========================
# TOKEN
# ========================

TOKEN = os.getenv("TOKEN")

# ========================
# INTENTS
# ========================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ========================
# CẤU HÌNH
# ========================

WELCOME_CHANNEL = "chung"  # đổi nếu cần
MUTE_DURATION = 60
MAX_WARN = 3

WELCOME_IMAGE = "https://media.giphy.com/media/OkJat1YNdoD3W/giphy.gif"
GOODBYE_IMAGE = "https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif"

toxic_words = ["ngu", "mkid", "oc cho", "do dien", "clan tao"]
toxic_count = defaultdict(int)

responses = [
    "😏 Emoji cũng không thoát đâu nha",
    "🚨 Nói chuyện lịch sự đi bạn",
    "🤨 Gắt vậy ai chơi?",
    "🧠 Bình tĩnh nào bro"
]

# ========================
# HÀM CHUẨN HOÁ TEXT
# ========================

def normalize_text(text):
    new_text = ""

    for char in text:
        if 0x1F1E6 <= ord(char) <= 0x1F1FF:
            new_text += chr(ord(char) - 0x1F1E6 + ord('a'))
        else:
            new_text += char

    new_text = unicodedata.normalize('NFD', new_text)
    new_text = ''.join(c for c in new_text if unicodedata.category(c) != 'Mn')

    return new_text.lower()

# ========================
# EVENTS
# ========================

@bot.event
async def on_ready():
    print(f"🔥 Whaley online: {bot.user}")

# ========================
# COMMANDS
# ========================

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓")

@bot.command()
async def toxic(ctx):
    count = toxic_count[ctx.author.id]
    await ctx.send(f"⚠ Bạn đã toxic {count} lần.")

# ========================
# MESSAGE FILTER
# ========================

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = normalize_text(message.content)

    if any(word in content for word in toxic_words):

        toxic_count[message.author.id] += 1

        # Xoá tin nhắn
        try:
            await message.delete()
        except:
            pass

        await message.channel.send(
            f"{message.author.mention} {random.choice(responses)}"
        )

        # Nếu quá giới hạn -> mute
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

# ========================
# WELCOME
# ========================

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name=WELCOME_CHANNEL)
    if not channel:
        return

    embed = discord.Embed(
        title="🎉 THÀNH VIÊN MỚI ĐÃ ĐẾN!!!",
        description=f"Chào mừng {member.mention} gia nhập 👏👏👏",
        color=discord.Color.purple()
    )

    embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
    embed.set_image(url=WELCOME_IMAGE)
    embed.set_footer(text="Welcome baby ❤️❤️❤️")

    await channel.send(embed=embed)

# ========================
# GOODBYE
# ========================

@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name=WELCOME_CHANNEL)
    if not channel:
        return

    embed = discord.Embed(
        title="💀 THÀNH VIÊN ĐÃ RỜI SERVER",
        description=f"{member.name} đã rời khỏi server rồi...",
        color=discord.Color.red()
    )

    embed.set_image(url=GOODBYE_IMAGE)
    embed.set_footer(text="Tạm biệt nhé 😢")

    await channel.send(embed=embed)

# ========================

bot.run(TOKEN)

