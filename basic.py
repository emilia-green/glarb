import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import random

dinner_outcomes = [
    "You eat dinner with Jay-Z. His business acumen is as sharp as his fashion sense, and you find yourself learning a lot about the music industry.",
    "You try to get dinner with Jay-Z, but he runs late due to an appointment at the helicopter dealership.",
    "You forgo the dinner and take the $50,000, using it to buy a solid gold CD copy of his 2008 album 'The Blueprint 3'.",
    "Jay-Z flies into a rage because the gazpacho soup is too cold. You are unable to glean any useful information from the dinner.",
    "Jay-Z explains to you how to whip coke over a stove using a Pyrex jug.",
    "Jay-Z explains that the famous clip of him nodding to a Timbaland beat was actually staged with a series of lifelike puppets.",
    "Jay-Z reveals that he is actually a time-traveling frog who has been manipulating the music industry for centuries, and that his real name is Glarb.",
    "Jay-Z narrowly defeats you in a rock-paper-scissors best of 7.",
    "You accidentally call Jay-Z 'Jay-G' and he is so offended that he cancels the dinner and leaves, leaving you with nothing but a $50,000 bill for the meal.",
    "You play the Jay-Z 'Monster' verse parody off your phone, and he does not find it funny. He leaves the dinner early, and you are left with a $50,000 bill for the meal.",
    "You play the Jay-Z 'Monster' verse parody off your phone, and he finds it hilarious. He laughs so hard that he accidentally chokes on his food and dies, leaving you with a $50,000 bill for the meal and a lifetime of guilt.",
]


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dinner")
    async def dinner(self, ctx):
        await ctx.send(dinner_outcomes[random.randint(0, len(dinner_outcomes) - 1)])

    @commands.command(name="commands")
    async def helpcmd(self, ctx):
        await ctx.send(
            "I am Glarb, the slipperiest sorcerer in the realm. I can play music and do some MtG related stuff. \n\n"
            "**Commands:**\n"
            "!play <video> - play a video\n"
            "!skip - skip the current video\n"
            "!stop - stop the music and disconnect\n"
            "!loop <video> - loop a video\n"
            "!playlist <name> - play a predefined playlist (battle or exploring)\n"
            "!shuffle - shuffle the current playlist\n"
            "!queue - show the current queue\n"
            "!dinner - have dinner with Jay-Z\n"
        )

    # doing something when the cog gets loaded
    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

    # doing something when the cog gets unloaded
    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded!")


async def setup(bot):
    # finally, adding the cog to the bot
    await bot.add_cog(Basic(bot=bot))
