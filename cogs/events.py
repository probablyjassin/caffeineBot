import os
from discord.ext import commands
from discord.utils import get
import discord

class events(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error): 
        if isinstance(error, commands.CommandNotFound): 
            await ctx.send(embed = discord.Embed(description=f"Command not found.", color=ctx.author.color))
        else:
            print(f"oh nein error und auch schlecht formatted weil ich will hja nicht gute logs: \n{error} \n")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if "balls" in message.content.lower():
            await message.channel.send(get(message.guild.emojis, name='balls'))
        elif "ball" in message.content.lower():
            await message.channel.send(get(message.guild.emojis, name='ball'))
        if "om" in (message.content.lower()).split(" "):
            await message.channel.send(get(message.guild.emojis, name='om'))
        if "ripbozo" in message.content.lower():
            await message.channel.send(get(message.guild.emojis, name='RIPBOZO'))
def setup(bot: commands.Bot):
    bot.add_cog(events(bot))