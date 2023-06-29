import os
import discord
from discord.ext import commands

class admin(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, filename = ""):
        if not filename:
            for filename in os.listdir('./cogs'):
                if not filename.endswith('.py'): continue
                self.bot.reload_extension(f'cogs.{filename[:-3]}')
                return await ctx.message.add_reaction("🤙")
                
        self.bot.reload_extension(f'cogs.{filename}')
        return await ctx.message.add_reaction("🤙")
        

    @commands.command(aliases = ['shut', 'close'])
    @commands.is_owner()
    async def shutdown(self, ctx):
        await self.bot.close()

def setup(bot: commands.Bot):
    bot.add_cog(admin(bot))