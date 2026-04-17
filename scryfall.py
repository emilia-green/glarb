from random import random

import discord
from discord.ext import commands
from dotenv import load_dotenv
import io
import random

url = "https://api.scryfall.com/cards/"

fetch_dialogue = [
    "I gaze into the swirling portents, and I see the following omen:", 
    "From the mists of my orb, a vision emerges:", 
    "I look into the tea leaves, and the tea looks back:", 
    "The entrails of some poor soul foretell this future calamity:",
    "My dowsing rod entreats this drop of knowledge to the surface:"]

wubrg_values = [
    'W',
    'U',
    'B',
    'R',
    'G'
]
WUBRG = ['WUBRG']



GUILD_NAMES = {
    # 2 colour
    'AZORIUS': 'WU',
    'DIMIR': 'UB',
    'RAKDOS': 'BR',
    'GRUUL': 'RG',
    'SELESNYA': 'GW',
    'ORZHOV': 'WB',
    'IZZET': 'UR',
    'GOLGARI': 'BG',
    'BOROS': 'RW',
    'SIMIC': 'GU',
    # 3 colour
    'BANT': 'GWU',
    'ESPER': 'WUB',
    'GRIXIS': 'UBR',
    'JUND': 'BRG',
    'NAYA': 'RGW',
    'MARDU': 'RWB',
    'TEMUR': 'RGU',
    'ABZAN': 'WBG',
    'JESKAI': 'WUR',
    'SULTAI': 'BGU',
    # 4 colour
    'NEPHALIA': 'WUBR',
    'YORE': 'WUBR',
    'GLINT': 'UBRG',
    'DUNE': 'WBRG',
    'INK': 'WURG',
    'WITCH': 'WUBG',
    # 5 colour
    'WUBRG': 'WUBRG',
    'ALL': 'WUBRG'
}

async def wubrg_sort(identity):
    return ''.join(sorted(identity, key=lambda x: wubrg_values.index(x)))


class Scryfall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded!")

    @commands.command(name="random")
    async def random(self, ctx):
        url = 'https://api.scryfall.com/cards/random'
        response = await self.bot.http_get(url, "json")

        image_url = response["image_uris"]["normal"]
        image_response = await self.bot.http_get(image_url, "img")
        image_file = discord.File(io.BytesIO(image_response), filename="card.png")

        await ctx.send(fetch_dialogue[int(random() * len(fetch_dialogue))] + "\n**" + response["name"] + "**", file=image_file)

    async def get_random_commander(self, identity: str):
        search_id = identity
        
        if search_id in GUILD_NAMES:
                    search_id = GUILD_NAMES[search_id]
                  
        url = f'https://api.scryfall.com/cards/random?q=id%3D{search_id}+is%3Acommander'
        data = await self.bot.http_get(url, return_type="json")

        # image_url = data["image_uris"]["normal"]
        # image_response = await self.bot.http_get_img(image_url)
        # image_file = discord.File(io.BytesIO(image_response), filename="card.png")


        return data
    
    @commands.group()
    async def commander(self, ctx):
        if ctx.invoked_subcommand is None:
            # default behavior is fetch any commander
            response = await self.bot.http_get(url + "random?q=is%3Acommander", "json")

            image_url = response["image_uris"]["normal"]
            image_response = await self.bot.http_get(image_url, "img")
            image_file = discord.File(io.BytesIO(image_response), filename="card.png")

            await ctx.send(random.choice(fetch_dialogue) + "\n**" + response["name"] + "**", file=image_file)

    @commands.command()
    async def commander(self, ctx, identity: str):
        normalised = identity.upper()

        if normalised in GUILD_NAMES:
            return_id = normalised
        else:
            normalised = ''.join(sorted(normalised, key=lambda x: wubrg_values.index(x)))
            if normalised not in GUILD_NAMES.values():
                await ctx.send("Invalid identity. Please provide a valid WUBRG combination or guild name.")
                return
            return_id = [key for key, value in GUILD_NAMES.items() if value == normalised]

        prefix = random.choice(fetch_dialogue)
        
        card = await self.get_random_commander(normalised)
        await ctx.send(f"{prefix} your random {return_id[0].capitalize()} commander is: **{card['name']}**\n{card['scryfall_uri']}")  


async def setup(bot):
    await bot.add_cog(Scryfall(bot=bot))