import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import io
import aiohttp

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dinner")
    async def dinner(self, ctx):
        await ctx.send("You eat dinner with Jay-Z Again.")

    @commands.command(name="ping")
    async def pingcmd(self, ctx):
        """the best command in existence"""
        await ctx.send(ctx.author.mention)

    # adding an event listener to the cog
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild and message.guild.me.guild_permissions.ban_members:
            await message.author.ban(reason="no speek") # very good reason
    # doing something when the cog gets loaded
    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

    # doing something when the cog gets unloaded
    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded!")




async def setup(bot):
        # finally, adding the cog to the bot
    await bot.add_cog(Greetings(bot=bot))