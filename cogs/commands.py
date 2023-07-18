import os
import discord
from discord.ext import commands
from reddit import reddit
import re
import aiohttp
import asyncio
import random
import json
import seventv
from seventv.seventv import seventvException
import string
import subprocess

class commandos(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.httpSession = aiohttp.ClientSession()
        print("Created http session")
        self.tv = seventv.seventv()
        print("Created 7tv session")

    def cog_unload(self):
        asyncio.run_coroutine_threadsafe(
            self.httpSession.close(), self.bot.loop
        ) 
        print("Closed http session")
        asyncio.run_coroutine_threadsafe(
            self.tv.close(), self.bot.loop
        )
        print("Closed 7tv session")

    @commands.command()
    async def rdt(self, ctx: commands.Context, arg = ""):
        async with ctx.typing():
            if not arg:
                return await ctx.send("Pick a subreddit")
            try:
                subreddit: reddit.subreddit = await reddit.subreddit(arg)
                submission = random.choice([meme async for meme in subreddit.hot(limit=50)])
                if submission.over_18 and not ctx.channel.is_nsfw(): return await ctx.send("We don't do that here, use an nsfw channel for that.")
            except:
                return await ctx.send("That subreddit does not exist")
            await asyncio.sleep(0.1)
        await ctx.send(submission.title)
        await ctx.send(submission.url)

    @commands.command()
    async def say(self, ctx: commands.Context, mentio, *, message = ""):
        if not mentio and message:
            return await ctx.send("Say what??")
        mention = re.match(r"<@([\d]+)>", mentio)
        if not mention:
            message = f'{mentio} {message}'
            imitate = ctx.message.author.id
        else:
            imitate = mention.group(1)
        member = await ctx.guild.fetch_member(imitate)
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
        async with ctx.typing():
            key = os.getenv('QUOTES_APIKEY')
            quoteTitle = str
            quoteAuthor = str
            if category.lower() == "undertale":
                with open("./files/undertale.json") as file:
                    data = json.load(file)
                    quote = random.choice(data)
                    quoteTitle = quote["quote"]
                    quoteAuthor = quote["author"]
                    return (
                        await ctx.send(embed = discord.Embed(
                            title = quoteTitle,
                            description = quoteAuthor,
                            color=ctx.author.color))
                    )
            category = f'?category={category}'
            async with self.httpSession.get(f"https://api.api-ninjas.com/v1/quotes{category.lower()}",
                headers = {'X-Api-Key': key},
                ) as resp:
                content = await resp.json()
            if not content:
                return (
                    await ctx.send(embed = discord.Embed(
                        description = "That didn't work\n Are you sure you used a valid category?"
                    ))
                )
            quoteTitle = content[0]["quote"]
            quoteAuthor = content[0]["author"]
            await ctx.send(embed = discord.Embed(title = quoteTitle, description = quoteAuthor, color=ctx.author.color))
        await asyncio.sleep(0.1)

    @commands.command(hidden=True)
    async def henti(self, ctx: commands.Context, type = 'sfw', category = "neko"):
        if type == 'nsfw' and not ctx.channel.is_nsfw():
            return await ctx.send("W- What are you trying to do? Do that in an nsfw channel you weirdo!")
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
    async def emote(self, ctx: commands.Context, *, query: str = ""):
        limit = 100 if not query else 20
        if not query: query = random.choice(string.ascii_letters)
        try:
            data = await self.tv.emote_search(query, limit, query="url")
        except seventvException	as error:
            await ctx.send("https://cdn.7tv.app/emote/6250b5ea2667140c8cedd1e9/2x.gif")
            return await ctx.send(embed = discord.Embed(description=re.sub(r'\d+', '', str(error)), color=ctx.author.color))
        if not data:
            await ctx.send("https://cdn.7tv.app/emote/60abf171870d317bef23d399/2x.gif")
            return await ctx.send(embed = discord.Embed(description="I didn't find any emotes", color=ctx.author.color))
        url = f'https:{random.choice(data).host_url}'
        async with self.httpSession.get(f'{url}/2x.gif') as response:
            if response.status != 200:
                return await ctx.send(f'{url}/2x.png')
            await ctx.send(f'{url}/2x.gif')

    @commands.command()
    async def clear(self, ctx: commands.Context, lim = 2):
        await ctx.channel.purge(limit=lim +1)

    @commands.command()
    async def hot(self, ctx: commands.Context):
        output, _ = subprocess.Popen("vcgencmd measure_temp", stdout=subprocess.PIPE, shell=True).communicate()
        temp = float(re.findall("\d+\.\d+", output.decode("utf-8"))[0])
        if temp >= 50: await ctx.send(f"Pretty toasty, I'm sitting at about {temp}°C")
        elif temp <= 40: await ctx.send(f"Wow, {temp}°C that's quite cool")
        else: await ctx.send(f"{temp}°C, that's pretty ok")

def setup(bot: commands.Bot):
    bot.add_cog(commandos(bot))