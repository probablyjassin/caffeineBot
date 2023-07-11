import discord
from discord.ext import commands

class help(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(name = "help-ping")
    async def helpi(self, ctx: commands.Context):
        await ctx.send(embed = discord.Embed(
            description = 'Bro "ping" "pong" was ist daran so schwer'
        ))

    @commands.command(name = "help-say")
    async def helpi(self, ctx: commands.Context):
        await ctx.send(embed = discord.Embed(
            title="say \{user to imitate (optional), message\}", 
            description="Sends a message of the provided text, as the user to imitate (if given)."
        ))

    @commands.command(name = "help-r")
    async def helpi(self, ctx: commands.Context):
        await ctx.send(embed = discord.Embed(
            title="r \{subreddit\}", 
            description="Get a reddit post from a subreddit of your choice"
        ))

    @commands.command(name = "help-quote")
    async def helpi(self, ctx: commands.Context):
        await ctx.send(embed = discord.Embed(
            title="quote \{category\} (optional)", 
            description="Get a quote, optionally with a category. " +
            "Categories include undertale, as well as these: https://api-ninjas.com/api/quotes"
        ))

    @commands.command(name = "help-emote")
    async def helpi(self, ctx: commands.Context):
        await ctx.send(embed = discord.Embed(
            title="emote \{name\} (optional)", 
            description="Search for 7tv emotes or get a random one!"
        ))

    @commands.command(name = "help-henti")
    async def helpi(self, ctx: commands.Context):
        await ctx.send(embed = discord.Embed(
            title="henti \{rating, category\} (optional)", 
            description="Get an some anime imagery. If unspecified, get an sfw catgirl. Optionally use nsfw and/or request a category. " +
            "Will use default if category is invalid. List of categories: https://pypi.org/project/WaifuPicsPython/"
        ))  

    @commands.command()
    async def help(self, ctx: commands.Context):
        bot = ctx.guild.get_member(self.bot.user.id)
        embed = discord.Embed(
            title = f'{bot.display_name} - commands',
            description = f'For detailed explanations use \n {self.bot.command_prefix}help.{{command}}'
        )
        embed.set_thumbnail(url=bot.display_avatar)
        embed.add_field(
            name = "Commands:", 
            value = f'''
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