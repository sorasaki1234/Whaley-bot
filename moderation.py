import discord
from discord.ext import commands
import json
import aiosqlite

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with open("config.json") as f:
            self.config = json.load(f)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.guild.system_channel.send(f"👋 Chào {member.mention} đến server!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        for word in self.config["bad_words"]:
            if word in message.content.lower():
                await message.delete()
                await message.channel.send(f"{message.author.mention} ⚠ Không nói bậy!")
                break

    @commands.command()
    async def warn(self, ctx, member: discord.Member):
        async with aiosqlite.connect("database.db") as db:
            await db.execute("""
            INSERT INTO users(user_id, warns)
            VALUES(?, 1)
            ON CONFLICT(user_id) DO UPDATE SET warns = warns + 1
            """, (member.id,))
            await db.commit()

        await ctx.send(f"{member.mention} đã bị cảnh cáo!")

async def setup(bot):
    await bot.add_cog(Moderation(bot))