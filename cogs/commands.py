import os
import discord
from discord.ext import commands
from reddit import reddit
import re
import aiohttp
import asyncio
import random
import json

class commandos(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.httpSession = aiohttp.ClientSession()
        print("[Info] created http session")

    def cog_unload(self):
        asyncio.run_coroutine_threadsafe(
            self.httpSession.close(), self.bot.loop
        )        
        print("[Info] closed http session")

    @commands.command()
    async def r(self, ctx: commands.Context, arg = ""):
        async with ctx.typing():
            if not arg:
                return await ctx.send("Pick a subreddit")
            try:
                subreddit = await reddit.subreddit(arg)
                submission = random.choice([meme async for meme in subreddit.hot(limit=50)])
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
                #params = {"category": category.lower()}
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

    @commands.command()
    async def test(self, ctx: commands.Context):

        gif_data = webp_to_gif("https://cdn.7tv.app/emote/60ae958e229664e8667aea38/4x.webp")
        await ctx.send(file=discord.File(gif_data, 'animated_image.gif'))

from PIL import Image
import requests
from io import BytesIO

def webp_to_gif(webp_url):
    response = requests.get(webp_url)
    webp_image = Image.open(BytesIO(response.content))

    # Convert the image to gif in memory
    gif_image = webp_image.convert('RGBA')
    gif_data = BytesIO()
    gif_image.save(gif_data, 'GIF')
    gif_data.seek(0)
    
    return gif_data

def setup(bot: commands.Bot):
    bot.add_cog(commandos(bot))