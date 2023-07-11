from discord.ext import commands
from discord.utils import get
import discord
from seventv.seventv import seventvException
import re

class events(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error): 
        if isinstance(error, commands.CommandNotFound): 
            await ctx.send(embed = discord.Embed(description="Command not found.", color=ctx.author.color))
        else:
            print(f"oh nein error und schlecht formatted weil ich will hja nicht gute logs: \n{error} \n")

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
        if "monkagiga" in message.content.lower():
            await message.channel.send(get(message.guild.emojis, name='monkaGIGA'))
        if "bavardage" in message.content.lower():
            with open("./files/bavardage.txt", "r") as counter:
                count = int(counter.read()) + 1
            with open("./files/bavardage.txt", "w") as counter:
                counter.write(str(count))
            await message.channel.send(f'{count} typos have been reported to the BavardagePolice')
            await message.channel.send("https://cdn.7tv.app/emote/630f73b6c7b627ebb036e7ee/2x.gif")

def setup(bot: commands.Bot):
    bot.add_cog(events(bot))