import discord
from discord.ext import commands
from reddit import os, reddit

intents = discord.Intents().all()
owners = [769525682039947314]

class customBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    async def close(self):
        for name,cog in self.cogs.items():
            cog._eject(self)
            print(f"Ejected {name}")
        await reddit.close()
        await super().close()

bot = customBot(
    command_prefix=".", case_insensitive = True, help_command = None,
    intents=intents, owner_ids = set(owners), 
    status=discord.Status.online, activity=discord.Game('(speedrunning)')
)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(os.getenv('DISCORD_TOKEN'))
    
# so hat's vorher funktioniert
# @bot.event 
# async def on_command_error(ctx, error): 
#     if isinstance(error, commands.CommandNotFound): 
#         await ctx.send(embed = discord.Embed(description=f"Command not found.", color=ctx.author.color))

