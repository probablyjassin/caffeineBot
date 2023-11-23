import requests
import os
import discord
from discord.ext import commands
from discord.utils import get
import json

from dotenv import load_dotenv
load_dotenv()


class gpt(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    def cog_unload(self):
        pass

    @commands.command()
    @commands.cooldown(5, 6000, commands.BucketType.user)
    async def gpt(self, ctx: commands.Context, *, message="briefly introduce yourself"):
        response = requests.post(
            f"{os.getenv('GPT_URL')}",
            stream=True,
            headers={
                "Authorization": f"Bearer {os.getenv('GPT_TOKEN')}"
            },
            json={
                "messages": [
                    {
                        "role": "system",
                        "content": """
                            You are Caffeine, a discord bot by Jässin.\n
                            You have various utility commands and can even stream music.\n
                            Keep your answers about 2 sentences short unless if you're asked complex questions or code samples.
                        """,
                    },
                    {"role": "user", "content": message},
                ],
                "stream": True,
                "model": "gpt-3.5-turbo",
                "temperature": 0.5,
                "presence_penalty": 0,
                "frequency_penalty": 0,
                "top_p": 1,
            },
        )

        message = await ctx.send("....")
        await message.add_reaction("〰️")
        text = ""

        if response.status_code == 200:
            for chunk in response.iter_lines():
                if chunk and chunk.decode("utf-8").startswith("data: {"):
                    obj: object = json.loads(
                        chunk.decode("utf-8").replace("data: ", "")
                    )
                    content = (
                        obj.get("choices", [{}])[0].get("delta", {}).get("content", "")
                    )

                    if len(content):
                        text += content
                        await message.edit(content=text)
        else:
            print(f"Error: {response.status_code}, {response.text}")
            await message.edit(
                content=f"An error occured, OpenAi returned a {response.status_code} response"
            )
        await message.clear_reaction("〰️")

    @gpt.error
    async def gpt_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"Currently on cooldown, try again in {int(error.retry_after/60)} minutes"
            )


def setup(bot: commands.Bot):
    bot.add_cog(gpt(bot))
