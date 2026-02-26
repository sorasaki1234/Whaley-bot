import discord
from discord.ext import commands
import json
import asyncio
from database import init_db

intents = discord.Intents.all()

with open("config.json") as f:
    config = json.load(f)

bot = commands.Bot(command_prefix=config["prefix"], intents=intents)

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")
    await init_db()

async def load_cogs():
    await bot.load_extension("cogs.moderation")
    await bot.load_extension("cogs.leveling")
    await bot.load_extension("cogs.ai_chat")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(config["token"])

asyncio.run(main())