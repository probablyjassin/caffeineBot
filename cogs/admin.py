import os
import sys
import subprocess
from discord.ext import commands

class admin(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, filename = ""):
        if not filename:
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    self.bot.reload_extension(f'cogs.{filename[:-3]}')
                    return await ctx.message.add_reaction("🤙")
        self.bot.reload_extension(f'cogs.{filename}')
        return await ctx.message.add_reaction("🤙")
        
    @commands.command()
    @commands.is_owner()
    async def reboot(self, ctx: commands.Context):
        await ctx.send("Rebooting...")
        await ctx.message.add_reaction("🤙")
        python = sys.executable
        subprocess.call([python, sys.argv[0]])
        sys.exit()

    @commands.command(aliases = ['shut', 'close'])
    @commands.is_owner()
    async def shutdown(self):
        await self.bot.close()

def setup(bot: commands.Bot):
    bot.add_cog(admin(bot))