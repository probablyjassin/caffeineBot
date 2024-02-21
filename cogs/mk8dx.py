import discord
import pymongo
from discord.ext import commands
from discord import slash_command

class mk8dx(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["admin"]
        self.collection = self.db["mk8dx"]

    def cog_unload(self):
        self.client.close()

    @slash_command(name="mmr", description="Retrieve the MMR of a given player")
    async def mk8dx(self, ctx: commands.Context, name: str):
        player = self.collection.find_one({"name": name})
        if player:
            await ctx.respond(f"{name}s MMR is {player['mmr']}")
        else:
            await ctx.respond(f"Couldn't find {name}s MMR")

    @slash_command(name="leaderboard", description="Show the leaderboard")
    #@commands.user_command(name="leaderboard", description="Show the leaderboard")
    async def leaderboard(self, ctx: discord.ApplicationContext, user: discord.user):
        data = self.collection.find()
        table_string = ""
        table_string += "```\n"
        table_string += " | Name       | MMR     | Wins | Losses |\n"
        table_string += " |------------|---------|-----|--------|\n"
        for player in data:
            table_string += f" | {player['name']:<20} | {player['mmr']:>5} | {player['wins']:>3} | {player['losses']:>3} |\n"
        table_string += "```"

        await ctx.respond(table_string)

    @commands.command()
    async def addPlayer(self, ctx: commands.Context):
        pass
        #documents = collection.find()
        #for doc in documents:
        #    print(doc)

        # Example: Insert a new document
        #new_document = {"name": "New Item", "value": 10}
        #collection.insert_one(new_document)

        # Example: Update a document
        #collection.update_one({"name": "Existing Item"}, {"$set": {"value": 20}})

        # Example: Delete a document
        #collection.delete_one({"name": "Item to Delete"})


def setup(bot: commands.Bot):
    bot.add_cog(mk8dx(bot))