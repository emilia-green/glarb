import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import io
import aiohttp
import requests

url = "https://api.scryfall.com/cards/"

class Scryfall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded!")

    @commands.command(name="random")
    async def random(self, ctx):
        response = requests.get(url + "random")
        data = response.json()

        image_url = data["image_uris"]["normal"]
        image_response = requests.get(image_url)
        image_file = discord.File(io.BytesIO(image_response.content), filename="card.png")

        await ctx.send("From my orb, I fetch the following portent:")
        await ctx.send("**" + data["name"] + "**", file=image_file)
    
    @commands.command(name="commander")
    async def commander(self, ctx):
        response = requests.get(url + "random?q=is%3Acommander")
        data = response.json()

        image_url = data["image_uris"]["normal"]
        image_response = requests.get(image_url)
        image_file = discord.File(io.BytesIO(image_response.content), filename="card.png")

        await ctx.send("From my orb, I fetch the following commander:")
        await ctx.send("**" + data["name"] + "**", file=image_file)




async def setup(bot):
        # finally, adding the cog to the bot
    await bot.add_cog(Scryfall(bot=bot))