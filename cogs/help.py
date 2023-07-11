import discord
from discord.ext import commands

class help(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(name = "help.ping")
    async def helpi(self, ctx: commands.Context):
        await ctx.send(embed = discord.Embed(
            value = 'Bro "ping" "pong" was ist daran so schwer'
        ))

    @commands.command(name = "help.say")
    async def helpi(self, ctx: commands.Context):
        await ctx.send(embed = discord.Embed(
            name="say \{user to imitate (optional), message\}", 
            value="Sends a message of the provided text, as the user to imitate (if given).", inline=False
        ))

    @commands.command(name = "help.r")
    async def helpi(self, ctx: commands.Context):
        await ctx.send(embed = discord.Embed(
            name="r \{subreddit\}", 
            value="Get a reddit post from a subreddit of your choice", inline=False
        ))

    @commands.command(name = "help.quote")
    async def helpi(self, ctx: commands.Context):
        await ctx.send(embed = discord.Embed(
            name="quote \{category\} (optional)", 
            value="Get a quote, optionally with a category. " +
            "Categories include undertale, as well as these: https://api-ninjas.com/api/quotes", inline=False
        ))

    @commands.command(name = "help.emote")
    async def helpi(self, ctx: commands.Context):
        await ctx.send(embed = discord.Embed(
            name="emote \{name\} (optional)", 
            value="Search for 7tv emotes or get a random one!", inline=False
        ))

    @commands.command(name = "help.henti")
    async def helpi(self, ctx: commands.Context):
        await ctx.send(embed = discord.Embed(
            name="henti \{rating, category\} (optional)", 
            value="Get an some anime imagery. If unspecified, get an sfw catgirl. Optionally use nsfw and/or request a category. " +
            "Will use default if category is invalid. List of categories: https://pypi.org/project/WaifuPicsPython/", inline=False
        ))  

    @commands.command()
    async def help(self, ctx: commands.Context):
        bot = ctx.guild.get_member(self.bot.user.id)
        embed = discord.Embed(
            title = f'{bot.display_name} - commands',
            description = f'For detailed explanations: \n help.{{command}}'
        )
        embed.set_thumbnail(url=bot.display_avatar)
        embed.add_field(
            name = "Commands:", 
            value = f''' \n
                ping
                say
                r (reddit)
                quote
                emote
                henti
            '''
        )
        await ctx.send(embed = embed)
        
def setup(bot: commands.Bot):
    bot.add_cog(help(bot))