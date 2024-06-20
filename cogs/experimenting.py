import discord
from discord import ApplicationContext, slash_command, Option
from discord.ui import Button, View
from discord.ext import commands

from waifu import WaifuAioClient

class test(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @slash_command(
        name="coolcommand",
        description="Sends an embed with an image and a delete button.",
    )
    async def coolcommand(self, ctx: ApplicationContext, nsfw = Option(str, name="nsfw", choices=['yes'], required=False)):
        picture = ""
        async with WaifuAioClient() as client:
            if nsfw:
                picture: str = await client.nsfw(category='waifu')
            else:    
                picture: str = await client.sfw(category='waifu')

        embed = discord.Embed(title="waifu")
        embed.set_image(url=picture)

        delete_button = discord.ui.Button(label="Delete", style=discord.ButtonStyle.red)

        view = discord.ui.View()
        view.add_item(delete_button)

        async def button_callback(interaction: discord.Interaction):
            if interaction.user == ctx.author or ctx.author.guild_permissions.administrator:
                await interaction.response.send_message("Image deleted!", ephemeral=True)
                await msg.delete()
            else:
                await interaction.response.send_message("You can't delete this image.", ephemeral=True)

        delete_button.callback = button_callback

        msg = await ((await ctx.respond(embed=embed, view=view)).original_response())

def setup(bot: commands.Bot):
    bot.add_cog(test(bot))