import asyncio
import re
from typing import Any
from pathlib import Path
from discord.ext import commands
import discord
import youtube_dl
import dotenv
from utils.embed_maker import EmbedMaker

ytdl_format_options: dict[str, Any] = {
    "format": "bestaudio",
}

ffmpeg_options = {
    "options": "-vn",
    "before_options": "-reconnect 1 -reocnnect_streamed 1 -reconnect_delay_max 5",
}

WORKDIR: Path = Path(__file__).parent.parent.parent


class MusicCog(commands.Cog):
    """Used to play music from YouTube."""

    def __init__(self, client: commands.Bot) -> None:
        """Constructor"""

        self.client: commands.Bot = client
        self.ytdl: youtube_dl.YoutubeDL = youtube_dl.YoutubeDL(ytdl_format_options)
        self.executable: Path = WORKDIR / "ffmpeg.exe"

        dotenv.load_dotenv()

    @commands.command(name="join")
    async def join(self, ctx: commands.Context) -> None:
        """Make the bot join an audio channel.

        Args:
            ctx (commands.Context): The context.
        """

        message: discord.Embed
        try:
            channel: discord.VoiceChannel = ctx.author.voice.channel
        except AttributeError:
            message = EmbedMaker.make_embed(
                name=f"Cannot join !",
                value="You must be in a vocal channel so i can join !",
            )
            await ctx.send(embed=message)
        else:
            if ctx.voice_client is None:
                await channel.connect()
            else:
                await ctx.voice_client.move_to(channel)

            message = EmbedMaker.make_embed(
                name="Succesfully joined",
                value=f"Joined channel : **{channel.mention}**",
            )
            await ctx.send(embed=message)

    @commands.command(name="leave")
    async def leave(self, ctx: commands.Context) -> None:
        """Make the bot leave the voice channel.

        Args:
            ctx (commands.Context): The context.
        """

        message: discord.Embed
        if ctx.voice_client is not None:
            message = EmbedMaker.make_embed(
                name="Succesfully left",
                value=f"Left the voice channel : {ctx.voice_client.channel.mention}",
            )
            await ctx.voice_client.disconnect()
            await ctx.send(embed=message)
        else:
            message = EmbedMaker.make_embed(
                name="Cannot left if not in a channel.",
                value="I must be in a voice channel to disconnect.",
            )
            await ctx.send(embed=message)

    @commands.command(name="play")
    async def play(self, ctx: commands.Context, *, arg: str) -> None:
        """Make the bot play a song from a YouTube URL or search for keyword.

        Args:
            ctx (commands.Context): The context.
            arg (str): The URL of the music.
        """

        message: discord.Embed
        try:
            if arg.startswith("http"):
                res: Any = self.ytdl.extract_info(arg, download=False)
                source_url: str = res.get("formats")[0].get("url")
                title: str = res.get("title")
                new_url: str = arg
            else:
                source_url, title, new_url = await self.from_str(ctx, arg=arg)
        except youtube_dl.DownloadError:
            message = EmbedMaker.make_embed(
                name="Error while attemptin to stream the music.",
                value=f"Error happenned for research with the keywords : {arg}",
            )
            await ctx.send(embed=message)

        if source_url:
            source = await discord.FFmpegOpusAudio.from_probe(source_url)
            ctx.voice_client.play(source)

            message = EmbedMaker.make_embed(
                name=f"Music playing.",
                value=f"Now playing [{title}]({new_url}), requested by {ctx.author.mention}",
            )
            await ctx.send(embed=message)

    async def from_str(self, ctx: commands.Context, *, arg: str):
        """Search Youtube for a list of music, based on keyword.

        Args:
            ctx (commands.Context): The context.
            arg (str): What to search.

        Returns:
            tuple: Contains the title, the source url for the music and the Yt url.
        """

        message: discord.Embed
        res: Any = self.ytdl.extract_info(f"ytsearch5:{arg}", download=False)["entries"]
        message = EmbedMaker.make_embed(
            name="Make your choices !",
            value=f"\n**:1** - {res[0].get('title')}\n"
            f"**:2** - {res[1].get('title')}\n**:3** - {res[2].get('title')}"
            f"\n**:4** - {res[3].get('title')}\n**:5** - {res[4].get('title')}\n",
        )
        await ctx.send(embed=message)

        try:
            msg = await self.client.wait_for(
                "message",
                check=lambda m: re.match(r"^:[012345]", m.content),
                timeout=15.0,
            )
        except asyncio.TimeoutError:
            message = EmbedMaker.make_embed(
                name="Request timed out.",
                value="Music request timed out, next time choose faster !",
            )
            await ctx.send(embed=message)
            return ("", "", "")  # Only so it don't raise an TypeError.
        else:
            await ctx.channel.purge(limit=1)

            ret: dict[str, Any] = res[int(msg.content[1:]) - 1]
            return (
                ret.get("formats")[0].get("url"),  # type: ignore
                ret.get("title"),
                ret.get("webpage_url"),
            )

    @commands.command(name="pause")
    async def pause(self, ctx: commands.Context) -> None:
        """Pause the music.

        Args:
            ctx (commands.Context): The context.
        """

        ctx.voice_client.pause()
        message: discord.Embed = EmbedMaker.make_embed(
            name=f"Music paused.",
            value=f"**Paused** the music, requested by {ctx.author.mention} !",
        )
        await ctx.send(embed=message)

    @commands.command(name="resume")
    async def resume(self, ctx: commands.Context) -> None:
        """Resume the music.

        Args:
            ctx (commands.Context): The context.
        """

        ctx.voice_client.resume()
        message: discord.Embed = EmbedMaker.make_embed(
            name=f"Music resumed.",
            value=f"**Resumed** the music, requested by {ctx.author.mention} !",
        )
        await ctx.send(embed=message)

    @commands.command(name="stop")
    async def stop(self, ctx: commands.Context) -> None:
        """Stop the music.

        Args:
            ctx (commands.Context): The context.
        """

        message: discord.Embed = EmbedMaker.make_embed(
            name=f"Music stopped.",
            value=f"**Stopped** the music ! And left {ctx.voice_client.channel.mention}, "
            f"requested by {ctx.author.mention}",
        )
        await ctx.voice_client.disconnect()
        await ctx.send(embed=message)

    @play.before_invoke
    async def ensure_voice(self, ctx: commands.Context) -> None:
        """Make sure the people calling play commands is in a voice channel.

        Args:
            ctx (commands.Context): The context.
        """

        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                message: discord.Embed = EmbedMaker.make_embed(
                    name=f"You must connect to a voice channel.",
                    value="You are not connected to a voice channel.",
                )
                await ctx.send(embed=message)
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()