import discord
from discord.ext import commands

class help(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command()
    async def help_ping(self, ctx: commands.Context):
        await ctx.send(embed = discord.Embed(
            description = 'Bro "ping" "pong" was ist daran so schwer?'
        ))

    @commands.command()
    async def help_say(self, ctx: commands.Context):
        await ctx.send(embed = discord.Embed(
            title="say \{user to imitate (optional), message\}", 
            description="Sends a message of the provided text, as the user to imitate (if given)."
        ))

    @commands.command()
    async def help_rdt(self, ctx: commands.Context):
        await ctx.send(embed = discord.Embed(
            title="rdt \{subreddit\}", 
            description="Get a reddit post from a subreddit of your choice"
        ))

    @commands.command()
    async def help_quote(self, ctx: commands.Context):
        await ctx.send(embed = discord.Embed(
            title="quote \{category\} (optional)", 
            description="Get a quote, optionally with a category. " +
            "Categories include undertale, as well as these: https://api-ninjas.com/api/quotes"
        ))

    @commands.command()
    async def help_emote(self, ctx: commands.Context):
        await ctx.send(embed = discord.Embed(
            title="emote \{name\} (optional)", 
            description="Search for 7tv emotes or get a random one!"
        ))

    @commands.command()
    async def help(self, ctx: commands.Context):
        bot = ctx.guild.get_member(self.bot.user.id)
        embed = discord.Embed(
            title = f'{bot.display_name} - commands',
            description = f'For detailed explanations use\n{self.bot.command_prefix}help_{{command}}'
        )
        embed.set_thumbnail(url=bot.display_avatar)
        embed.add_field(
            name = "Commands:", 
            value = f'''
            ping
            say
            rdt (reddit)
            quote
            emote
            '''
        )
        await ctx.send(embed = embed)
        
def setup(bot: commands.Bot):
    bot.add_cog(help(bot))