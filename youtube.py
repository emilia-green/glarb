import asyncio
import discord
from discord.ext import commands
import yt_dlp
import random


ytdlp_options = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": False,
    "extractor_args": {"youtube": {"skip": ["dash", "hls"]}},
    "ignoreerrors": True,
    "extract_flat": True,
}

voice_clients = {}
ytdl = yt_dlp.YoutubeDL(ytdlp_options)
ffmpeg_options = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}

playlists = {
    "battle": "https://www.youtube.com/playlist?list=PLkYCZ4ZCoNzC2n1WeeGsneVq_t47KuTms",
    "exploring": "https://www.youtube.com/playlist?list=PLkYCZ4ZCoNzD4VBov0fkAzGLMyUmP-4KB",
}


class YTDLP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.looping = False

    def voice_check(self, ctx):
        if not ctx.author.voice:
            return (
                False,
                "Foolish tadpole, you need to be in a voice channel to play music.",
            )
        return True, None

    async def initialise_voice_client(self, ctx):
        if ctx.guild.id not in voice_clients:
            voice_client = await ctx.author.voice.channel.connect()
            voice_clients[ctx.guild.id] = voice_client

    @commands.command()
    async def playlist(self, ctx, playlist_name: str):

        is_valid, error_message = self.voice_check(ctx)
        if not is_valid:
            await ctx.send(error_message)
            return

        if playlist_name not in playlists:
            await ctx.send(
                "Invalid playlist name, foolish pond scum. Glarb is currently configured for two playlists: 'battle' and 'exploring'. Attach one of them at the end of !play."
            )
            return

        url = playlists[playlist_name]
        loop = asyncio.get_event_loop()

        await self.initialise_voice_client(ctx)

        try:

            data = await loop.run_in_executor(
                None, lambda: ytdl.extract_info(url, download=False)
            )

            self.queue = [e for e in data["entries"] if e is not None]
            entry = self.queue.pop(0)
            video_data = await loop.run_in_executor(
                None, lambda: ytdl.extract_info(entry["url"], download=False)
            )

            if video_data is None:
                await self.play_next(ctx)
                return

            audio_url = video_data["url"]

        except Exception as e:
            await ctx.send(
                f"Despite the efforts of my greatest seers, an error occurred while trying to fetch the audio: {str(e)}"
            )
            await self.play_next(ctx)
            return

        # join audio and play the music
        try:
            if audio_url is None:
                await ctx.send(
                    "My augurs could not find a valid audio stream for this video. Moving on to the next one."
                )
                await self.play_next(ctx)
                return

            player = discord.FFmpegPCMAudio(audio_url, **ffmpeg_options)
            source = discord.PCMVolumeTransformer(player, volume=0.5)

            await ctx.send(f"Now playing: {video_data.get('title', 'Unknown')}")
            voice_clients[ctx.guild.id].play(
                source,
                after=lambda e: (print(f"Player error: {e}") if e else None)
                or asyncio.run_coroutine_threadsafe(self.play_next(ctx), loop),
            )

        except Exception as e:
            await ctx.send(
                f"Despite the toil of my finest augurs, an error occurred while trying to play the audio: {str(e)}"
            )

    async def play_next(self, ctx):

        if not self.queue:
            await ctx.send("The playlist has come to an end, my supplicant.")

        entry = self.queue.pop(0)
        if self.looping:
            self.queue.append(entry)

        try:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(
                None, lambda: ytdl.extract_info(entry["url"], download=False)
            )
            if data is None:
                await self.play_next(ctx)
                return

            audio_url = data["url"]
        except Exception as e:
            await ctx.send(f"Glarb could not divine the next track: {str(e)}")
            await self.play_next(ctx)
            return

        player = discord.FFmpegPCMAudio(audio_url, **ffmpeg_options)
        source = discord.PCMVolumeTransformer(player, volume=0.5)

        if not self.looping:
            await ctx.send(f"Now playing: {data.get('title', 'Unknown')}")
        else:
            await ctx.send(
                f"My choir of toads are looping the following track: {data.get('title', 'Unknown')}"
            )

        loop = asyncio.get_event_loop()
        voice_clients[ctx.guild.id].play(
            source,
            after=lambda e: (print(f"Player error: {e}") if e else None)
            or asyncio.run_coroutine_threadsafe(self.play_next(ctx), loop),
        )

    @commands.command(name="skip")
    async def skip(self, ctx):
        if ctx.guild.id in voice_clients and voice_clients[ctx.guild.id].is_playing():
            await ctx.send("Skipping to the next track.")
            voice_clients[ctx.guild.id].stop()
        else:
            await ctx.send("There is no track currently playing, insect.")

    @commands.command(name="loop")
    async def loop(self, ctx, video: str):
        is_valid, error_message = self.voice_check(ctx)
        if not is_valid:
            await ctx.send(error_message)
            return
        self.queue = [{"url": video}]
        self.looping = True
        await self.initialise_voice_client(ctx)
        await self.play_next(ctx)

    @commands.command(name="play")
    async def play(self, ctx, video: str):
        is_valid, error_message = self.voice_check(ctx)
        if not is_valid:
            await ctx.send(error_message)
            return
        if ctx.guild.id in voice_clients and voice_clients[ctx.guild.id].is_playing():
            self.queue.append({"url": video})
            await ctx.send("The track has been added to the queue, my tadpole.")
            return
        self.queue = [{"url": video}]
        self.looping = False
        await self.initialise_voice_client(ctx)
        await self.play_next(ctx)

    @commands.command(name="stop")
    async def stop(self, ctx):
        if ctx.guild.id in voice_clients:
            self.queue = []
            self.looping = False
            voice_clients[ctx.guild.id].stop()
            await voice_clients[ctx.guild.id].disconnect()
            del voice_clients[ctx.guild.id]
            await ctx.send("Going back to my pond.")

    @commands.command(name="shuffle")
    async def shuffle(self, ctx):
        if not self.queue:
            await ctx.send("The playlist is currently empty, my tadpole.")
            return

        random.shuffle(self.queue)
        await ctx.send("The order of the playlist has been shuffled, my tadpole.")

    @commands.command(name="queue")
    async def show_queue(self, ctx):
        if not self.queue:
            await ctx.send("The playlist is currently empty, my tadpole.")
            return

        queue_titles = []
        loop = asyncio.get_event_loop()
        for entry in self.queue:
            try:
                data = await loop.run_in_executor(
                    None, lambda: ytdl.extract_info(entry["url"], download=False)
                )
                title = data.get("title", "Unknown")
                queue_titles.append(title)
            except Exception as e:
                queue_titles.append("Unknown")

        queue_message = "Current playlist:\n" + "\n".join(
            f"{idx + 1}. {title}" for idx, title in enumerate(queue_titles)
        )
        await ctx.send(queue_message)


async def setup(bot):
    # finally, adding the cog to the bot
    await bot.add_cog(YTDLP(bot=bot))
