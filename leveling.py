import discord
from discord.ext import commands
import aiosqlite
import random


class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def add_exp(self, user_id, amount):
        async with aiosqlite.connect("database.db") as db:
            await db.execute("""
            INSERT INTO users(user_id, exp)
            VALUES(?, ?)
            ON CONFLICT(user_id) DO UPDATE SET exp = exp + ?
            """, (user_id, amount, amount))
            await db.commit()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        await self.add_exp(message.author.id, random.randint(5, 10))

    @commands.command()
    async def rank(self, ctx):
        async with aiosqlite.connect("database.db") as db:
            async with db.execute("SELECT exp FROM users WHERE user_id = ?", (ctx.author.id,)) as cursor:
                row = await cursor.fetchone()

        if not row:
            return await ctx.send("Bạn chưa có EXP!")

        exp = row[0]
        level = int((exp / 100) ** 0.5)

        await ctx.send(f"📊 Level: {level} | EXP: {exp}")


async def setup(bot):
    await bot.add_cog(Leveling(bot))