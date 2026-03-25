import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import io
import aiohttp

# idea of events vs commands. Events are when things happen, but commands are like talking directly to the bot
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

class Glarb(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.load_extension("scryfalling")
        print("Loaded cogs smile")

async def main():
     bot = Glarb()
     async with bot:
          await bot.start(token)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())