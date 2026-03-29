from random import random

import discord
from discord.ext import commands
from dotenv import load_dotenv
import io

url = "https://api.scryfall.com/cards/"

VALID_COLOURS = set('WUBRG')
fetch_dialogue = [
    "I gaze into the swirling portents, and I see the following omen:", 
    "From the mists of my orb, a vision emerges:", 
    "I look into the tea leaves, and the tea looks back:", 
    "The entrails of some poor soul foretell this future calamity:",
    "My dowsing rod entreats this drop of knowledge to the surface:"]

GUILD_NAMES = {
    # 2 colour
    'azorius': 'WU',
    'dimir': 'UB',
    'rakdos': 'BR',
    'gruul': 'RG',
    'selesnya': 'GW',
    'orzhov': 'WB',
    'izzet': 'UR',
    'golgari': 'BG',
    'boros': 'RW',
    'simic': 'GU',
    # 3 colour
    'bant': 'GWU',
    'esper': 'WUB',
    'grixis': 'UBR',
    'jund': 'BRG',
    'naya': 'RGW',
    'mardu': 'RWB',
    'temur': 'RGU',
    'abzan': 'WBG',
    'jeskai': 'WUR',
    'sultai': 'BGU',
    # 4 colour
    'nephalia': 'WUBR',
    'yore': 'WUBR',
    'glint': 'UBRG',
    'dune': 'WBRG',
    'ink': 'WURG',
    'witch': 'WUBG',
    # 5 colour
    'wubrg': 'WUBRG',
    'all': 'WUBRG'
}



class Scryfall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded!")

    async def get_random_commander(self, identity: str):
        identity = ''.join(sorted(set(identity.upper())))
        
        # if not identity or not set(identity).issubset(VALID_COLOURS):
        #     return None, "Invalid colour identity. Use letters from W, U, B, R, G."
        
        url = 'https://api.scryfall.com/cards/random'
        params = {'q': f'id={identity} is:commander'}
        
        
        data = await self.bot.http_get(url, params=params, type="json")

        # image_url = data["image_uris"]["normal"]
        # image_response = await self.bot.http_get_img(image_url)
        # image_file = discord.File(io.BytesIO(image_response), filename="card.png")


        return data, None

    @commands.command(name="random")
    async def random(self, ctx):
        response = await self.bot.http_get(url + "random", "json")

        image_url = response["image_uris"]["normal"]
        image_response = await self.bot.http_get(image_url, "img")
        image_file = discord.File(io.BytesIO(image_response), filename="card.png")

        await ctx.send(fetch_dialogue[int(random() * len(fetch_dialogue))] + "\n**" + response["name"] + "**", file=image_file)

    
    @commands.group()
    async def commander(self, ctx):
        if ctx.invoked_subcommand is None:
            # default behavior is fetch any commander
            response = await self.bot.http_get(url + "random?q=is%3Acommander", "json")

            image_url = response["image_uris"]["normal"]
            image_response = await self.bot.http_get(image_url, "img")
            image_file = discord.File(io.BytesIO(image_response), filename="card.png")

            await ctx.send(fetch_dialogue[int(random() * len(fetch_dialogue))] + "\n**" + response["name"] + "**", file=image_file)
    
    @commands.command()
    async def commander2(self, ctx, identity: str):
        card, error = await self.get_random_commander(identity)
        
        if error:
            await ctx.send(error)
            return
        
        await ctx.send(f"Your random {identity.upper()} commander is: **{card['name']}**\n{card['scryfall_uri']}")
    
    # @commander.command(name="gruul")
    # async def gruul(self, ctx): 
    #     response = await self.bot.http_get_json(url + "random?q=id%3DGR+is%3Acommander")

    #     image_url = response["image_uris"]["normal"]
    #     image_response = await self.bot.http_get_img(image_url)
    #     image_file = discord.File(io.BytesIO(image_response), filename="card.png")

    #     await ctx.send("I look into the swirling portents, and I fetch the following Gruul commander:")
    #     await ctx.send("**" + response["name"] + "**", file=image_file)

    




async def setup(bot):
    await bot.add_cog(Scryfall(bot=bot))