from discord.ext import commands
import discord
import re
import unicodedata
from database import load_data, save_data

TOXIC_WORDS = ["ngu", "mkid", "cltao", "occho"]

def normalize(text):
    text = text.lower()

    def convert(match):
        return chr(ord(match.group(0)) - 127397)

    text = re.sub(r'[\U0001F1E6-\U0001F1FF]', convert, text)

    text = unicodedata.normalize("NFD", text)
    text = ''.join(c for c in text if unicodedata.category(c) != "Mn")

    text = re.sub(r'[^a-z]', '', text)

    return text

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel:
            embed = discord.Embed(
                title="🎉 THÀNH VIÊN MỚI ĐÃ ĐẾN!!!",
                description=f"Chào mừng {member.mention} đến với server!",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
            embed.set_image(url="https://media.giphy.com/media/OkJat1YNdoD3W/giphy.gif")
            embed.set_footer(text="Welcome baby ❤️❤️❤️")

            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.system_channel
        if channel:
            embed = discord.Embed(
                title="💀 THÀNH VIÊN ĐÃ RỜI SERVER",
                description=f"{member.name} đã rời khỏi server...",
                color=discord.Color.red()
            )
            embed.set_image(url="https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif")
            embed.set_footer(text="Tạm biệt nhé 😢")

            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        clean = normalize(message.content)

        for word in TOXIC_WORDS:
            if word in clean:
                data = load_data()
                user = str(message.author.id)

                if user not in data:
                    data[user] = {"xp": 0, "level": 1, "warn": 0}

                data[user]["warn"] += 1
                save_data(data)

                await message.delete()
                await message.channel.send(
                    f"⚠ {message.author.mention} bình tĩnh nào bro 😎"
                )

                if data[user]["warn"] >= 3:
                    role = discord.utils.get(message.guild.roles, name="Muted")
                    if role:
                        await message.author.add_roles(role)
                        await message.channel.send("🔇 Bạn đã bị mute 60s")
                        await message.author.timeout(
                            discord.utils.utcnow() + discord.timedelta(seconds=60)
                        )

                break

async def setup(bot):
    await bot.add_cog(Moderation(bot))
