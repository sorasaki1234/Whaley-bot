import discord
from discord.ext import commands
import os
import asyncio

# ===== LẤY TOKEN TỪ RAILWAY ENV =====
TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    raise ValueError("TOKEN not found in environment variables!")

# ===== INTENTS =====
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== EVENT =====
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    print("Bot is online and running on Railway 🚀")

# ===== TEST COMMAND =====
@bot.command()
async def ping(ctx):
    await ctx.send("Pong 🏓")

# ===== RUN BOT =====
bot.run(TOKEN)
