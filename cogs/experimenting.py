import discord
from discord import ApplicationContext, slash_command
from discord.ui import Button, View
from discord.ext import commands

async def send_image_with_delete(ctx, image_url):
        """Sends an image with a delete button."""
        # Create an embed with the image
        embed = discord.Embed(title="Image", image=image_url)

        # Define the delete button
        delete_button = Button(label="Delete", style=discord.ButtonStyle.red, custom_id="delete_image")

        # Create a view to hold the button
        view = View(timeout=None)  # Set timeout to None for persistent button
        view.add_item(delete_button)

        # Send the message with embed and view
        message = await ctx.send(embed=embed, view=view)

        # Handle button interaction (separate function for clarity)
        @view.callback
        async def delete_image_callback(interaction: discord.Interaction, button: discord.Button):
            if interaction.user == ctx.author:  # Check if user matches command invoker
                await message.delete()
                await interaction.response.send_message("Image deleted.", ephemeral=True)  # Ephemeral message disappears after a short time
            else:
                await interaction.response.send_message("You cannot delete this image.", ephemeral=True)


class test(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @slash_command(
        name="coolcommand",
        description="Sends an embed with an image and a delete button."
    )
    async def coolcommand(self, ctx: ApplicationContext):
        # Embed with image and title
        embed = discord.Embed(title="This is an image!", url="https://cdn.donmai.us/original/18/92/__original_drawn_by_hamu_plot_sy__18920206678d737dc5fa52ad746ee45a.jpg")
        embed.set_image(url="https://cdn.donmai.us/original/18/92/__original_drawn_by_hamu_plot_sy__18920206678d737dc5fa52ad746ee45a.jpg")  # Replace with your image URL

        # Define the delete button
        delete_button = discord.ui.Button(label="Delete", style=discord.ButtonStyle.red)

        # Create a view to hold the button and handle its click
        view = discord.ui.View()
        view.add_item(delete_button)

        # Async function to handle button click
        async def button_callback(interaction: discord.Interaction):
            if interaction.user == ctx.author:  # Check if button is clicked by the command user
                await interaction.response.send_message("Image deleted!", ephemeral=True)
                await msg.delete()
            else:
                await interaction.response.send_message("You can't delete this image.", ephemeral=True)

        delete_button.callback = button_callback

        msg = await ((await ctx.respond(embed=embed, view=view)).original_response())

def setup(bot: commands.Bot):
    bot.add_cog(test(bot))