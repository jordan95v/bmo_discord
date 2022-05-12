from discord.ext import commands
import discord
import os
from utils.embed_creator import EmbedCreator
from utils.help import HELP


class EventCog(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        """Constructor"""

        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        """Happen when the bot is connected and ready to be used."""

        await self.client.change_presence(
            activity=discord.Game(f"Sea of Pringles Thieves")
        )
        print(
            f"Logged as {self.client.user}, to {len(self.client.guilds)} "
            f"guild{'s' if len(self.client.guilds) >= 2 else ''}"
        )

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        """Happens when an error occur.

        Args:
            ctx (commands.Context): The context.
            errors (commands.CommandError): The error.
        """

        message: discord.Embed
        if isinstance(error, commands.errors.MissingRequiredArgument):
            message = EmbedCreator.create_embed(
                name=f"Arguments missing",
                value=f"{ctx.author.mention} ! You need to give me an arguments !",
            )
            await ctx.send(embed=message)

        chan_id: str = os.getenv("LOG_CHANNEL")  # type: ignore
        channel: discord.TextChannel = self.client.get_channel(id=int(chan_id))
        message = EmbedCreator.create_embed(
            name=f"An error occured.",
            value=f"Command made by {ctx.message.author}.\n**Command**: "
            f"{ctx.message.clean_content}.\n**Error**: {error}",
        )
        await channel.send(embed=message)

    @commands.command(name="help")
    async def help(self, ctx: commands.Context):
        """Show the help message.

        Args:
            ctx (commands.Context): The context.
        """

        message: discord.Embed = discord.Embed(
            title="Help", description="Show the list of commands available."
        )

        for element in HELP:
            message.add_field(name=element["name"], value=element["value"])

        await ctx.send(embed=message)
