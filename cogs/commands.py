import os
import discord
from discord.ext import commands
from auth import reddit
import fnmatch
import re
import aiohttp
import asyncio
import random
import json

class commandos(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.httpSession = aiohttp.ClientSession()
        print("[Info] created http session")        # MACH EINFACH LOGGING BRO
                                                    # NICHT PSEUDO LOGGING!!!

    def cog_unload(self):
        asyncio.run_coroutine_threadsafe(
            self.httpSession.close(), self.bot.loop
        )        

    @commands.command()
    async def r(self, ctx: commands.Context, arg = ""):
        if not arg:
            return await ctx.send("Pick a subreddit")
        try:
            subreddit = await reddit.subreddit(arg)
            submission = random.choice([meme async for meme in subreddit.hot(limit=50)])
        except:
            return await ctx.send("That subreddit does not exist")
        await ctx.send(submission.title)
        await ctx.send(submission.url)

    @commands.command()
    async def say(self, ctx: commands.Context, mentio, *, message = ""):
        if not mentio and message:
            return await ctx.send("Say what??")
        
        if not fnmatch.filter(mentio.split(" "), '<@*>'):
            message = f'{mentio} {message}'
            imitate = ctx.message.author.id
        else:
            imitate = int(''.join(re.findall(r'\d+', mentio)))

        member = ctx.guild.get_member(imitate)
        webhook = await ctx.channel.create_webhook(name=member.display_name)
        await webhook.send(
            message,
            username=member.display_name,
            avatar_url=member.display_avatar.url
        )
        await webhook.delete()
        await ctx.message.delete()

    @commands.command()
    async def quote(self, ctx: commands.Context, category = ""):
        key = os.getenv('QUOTES_APIKEY')
        quoteTitle = str
        quoteAuthor = str
        if category.lower() != "undertale":
            category = '?category=' + category.lower()
            try:
                async with self.httpSession.get(f"https://api.api-ninjas.com/v1/quotes{category}",
                                        headers = {'X-Api-Key': key}) as resp:
                    if resp.status == 200:
                        quoteTitle = (await resp.json())[0]["quote"]
                        quoteAuthor = (await resp.json())[0]["author"]
            except Exception as err:   
                await ctx.send(embed = discord.Embed(description = f"That didn't work\n{err}"))
        else:
            with open("./files/undertale.json") as file:
                data = json.load(file)
                quote = random.choice(data)
                quoteTitle = quote["quote"]
                quoteAuthor = quote["author"]
        await ctx.send(embed = discord.Embed(title = quoteTitle, description = quoteAuthor, color=ctx.author.color))

    @commands.command(hidden=True)
    async def henti(self, ctx: commands.Context, type = 'sfw', category = "neko"):
            async def neko(type, category):
                async with self.httpSession.get(f'https://api.waifu.pics/{type}/{category}') as response:
                    await ctx.send((await response.json())["url"])
            if type not in ["sfw", "nsfw"]:
                category = type
                type = 'sfw'
            try:
                await neko(type, category)
            except:
                await neko(type, "neko")

    @commands.command()
    async def clear(self, ctx: commands.Context, lim = 2):
        await ctx.channel.purge(limit=lim)

def setup(bot: commands.Bot):
    bot.add_cog(commandos(bot))