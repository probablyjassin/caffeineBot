import discord
from discord.ext import commands

class help(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command()
    async def help(self, ctx: commands.Context):
        bot = ctx.guild.get_member(self.bot.user.id)
        embed = discord.Embed(
            title = f'{bot.display_name} - commands',
        )
        embed.set_thumbnail(url=bot.display_avatar)
        embed.add_field(
            name="ping", 
            value="respond with pong", inline=False
        )
        embed.add_field(
            name="say (user to imitate and/or message)", 
            value="Sends a message of the provided text, as the user to imitate (if given).", inline=False
        )
        embed.add_field(
            name="quote (category)", 
            value="Get a quote, optionally with a category. " +
            "Categories include undertale, as well as these: https://api-ninjas.com/api/quotes", inline=False
        )
        embed.add_field(
            name="henti (rating, category)", 
            value="Get an some anime imagery. If unspecified, get an sfw catgirl. Optionally use nsfw and/or request a category. " +
            "Will use default if category is invalid. List of categories: https://pypi.org/project/WaifuPicsPython/", inline=False
        )
        await ctx.send(embed = embed)
        

def setup(bot: commands.Bot):
    bot.add_cog(help(bot))