import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

async def load_extensions():
    await bot.load_extension("leveling")
    await bot.load_extension("moderation")

async def main():
    async with bot:
        await load_extensions()
        token = os.getenv("TOKEN")
        
        if token is None:
            print("❌ TOKEN chưa được set trong Railway Variables!")
            return
        
        await bot.start(token)

asyncio.run(main())
