from discord.ext import commands
from database import load_data, save_data

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        data = load_data()
        user = str(message.author.id)

        if user not in data:
            data[user] = {"xp": 0, "level": 1, "warn": 0}

        data[user]["xp"] += 10

        if data[user]["xp"] >= data[user]["level"] * 100:
            data[user]["level"] += 1
            data[user]["xp"] = 0
            await message.channel.send(
                f"🎉 {message.author.mention} đã lên level {data[user]['level']}!"
            )

        save_data(data)

    @commands.command()
    async def lv(self, ctx):
        data = load_data()
        user = str(ctx.author.id)

        if user not in data:
            await ctx.send("Bạn chưa có level 😅")
            return

        xp = data[user]["xp"]
        level = data[user]["level"]

        await ctx.send(
            f"📊 {ctx.author.mention}\n"
            f"Level: {level}\n"
            f"XP: {xp}/{level*100}"
        )

async def setup(bot):
    await bot.add_cog(Leveling(bot))
