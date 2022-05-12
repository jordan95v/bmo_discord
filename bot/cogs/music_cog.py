import asyncio
import re
from typing import Any
from pathlib import Path
from discord.ext import commands
import discord
import youtube_dl
import dotenv
from utils.embed_creator import EmbedCreator

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
            message = EmbedCreator.create_embed(
                name=f"Cannot join !",
                value="You must be in a vocal channel so i can join !",
            )
        else:
            if ctx.voice_client is None:
                await channel.connect()
            else:
                await ctx.voice_client.move_to(channel)
            message = EmbedCreator.create_embed(
                name="Succesfully joined",
                value=f"Joined channel : **{channel.mention}**",
            )
        finally:
            await ctx.send(embed=message)

    @commands.command(name="leave")
    async def leave(self, ctx: commands.Context) -> None:
        """Make the bot leave the voice channel.

        Args:
            ctx (commands.Context): The context.
        """

        message: discord.Embed
        if ctx.voice_client is not None:
            message = EmbedCreator.create_embed(
                name="Succesfully left",
                value=f"Left the voice channel : {ctx.voice_client.channel.mention}",
            )
            await ctx.voice_client.disconnect()
        else:
            message = EmbedCreator.create_embed(
                name="Cannot left if not in a channel.",
                value="I must be in a voice channel to disconnect.",
            )
        await ctx.send(embed=message)

    @commands.command(name="play")
    async def play(self, ctx: commands.Context, *, arg: str) -> None:
        """Make the bot play a song from a YouTube URL or search for keyword.

        Args:
            ctx (commands.Context): The context.
            arg (str): The URL | keyword of the music.
        """

        message: discord.Embed
        ret: dict[str, str] = await self.download_source(ctx, arg)
        source: str = ret.get("source", "")
        title: str = ret.get("title", "")
        url: str = ret.get("url", arg)

        if source:
            music_source: discord.FFmpegOpusAudio = (
                await discord.FFmpegOpusAudio.from_probe(source)
            )
            ctx.voice_client.play(music_source)
            message = EmbedCreator.create_embed(
                name=f"Music playing.",
                value=f"Now playing [{title}]({url}), requested by {ctx.author.mention}",
            )
        await ctx.send(embed=message)

    async def download_source(self, ctx: commands.Context, arg):
        """Download music from either a url or keyword.

        Args:
            ctx (commands.Context): The context.
            arg (str): The URL | keyword of the music.
        """
        try:
            if arg.startswith("http"):
                return await self.from_url(ctx, arg=arg)
            else:
                return await self.from_str(ctx, arg=arg)

        except youtube_dl.DownloadError:
            message = EmbedCreator.create_embed(
                name="Error while attempting to stream the music.",
                value=f"Error happenned for research with the keywords : {arg}",
            )
            await ctx.send(embed=message)
            return dict()

    async def from_url(self, ctx: commands.Context, *, arg: str):
        """Search Youtube for an url.

        Args:
            arg (str): The url to search.

        Returns:
            tuple: Contains the title and the source url.
        """

        res: Any = self.ytdl.extract_info(arg, download=False)
        return dict(source=res.get("formats")[0].get("url"), title=res.get("title"))

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
        message = EmbedCreator.create_embed(
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
            message = EmbedCreator.create_embed(
                name="Request timed out.",
                value="Music request timed out, next time choose faster !",
            )
            await ctx.send(embed=message)
            return dict()
        else:
            await ctx.channel.purge(limit=1)
            ret: dict[str, Any] = res[int(msg.content[1:]) - 1]
            return dict(
                source=ret.get("formats")[0].get("url"),  # type: ignore
                title=ret.get("title"),
                url=ret.get("webpage_url"),
            )

    @commands.command(name="pause")
    async def pause(self, ctx: commands.Context) -> None:
        """Pause the music.

        Args:
            ctx (commands.Context): The context.
        """

        ctx.voice_client.pause()
        message: discord.Embed = EmbedCreator.create_embed(
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
        message: discord.Embed = EmbedCreator.create_embed(
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

        message: discord.Embed = EmbedCreator.create_embed(
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
                message: discord.Embed = EmbedCreator.create_embed(
                    name=f"You must connect to a voice channel.",
                    value="You are not connected to a voice channel.",
                )
                await ctx.send(embed=message)
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
