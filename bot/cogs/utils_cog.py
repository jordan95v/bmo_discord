from discord.ext import commands
import discord
import random
from utils.embed_creator import EmbedCreator


class UtilsCog(commands.Cog):
    """Contains utils commands."""

    def __init__(self, client: commands.Bot) -> None:
        """Constructor"""

        self.client: commands.Bot = client

    @commands.command(name="pin")
    async def pin_message(self, ctx: commands.Context) -> None:
        """Pin a message from a discord channel.

        Args:
            ctx (commands.Context): The context.
        """

        messages = await ctx.channel.history(limit=2).flatten()
        await messages[-1].pin()
        await ctx.channel.purge(limit=1)
        message: discord.Embed = EmbedCreator.create_embed(
            name=f"Messages pinned",
            value=f"{ctx.author.mention} pinned a message from {messages[-1].author.mention} !",
        )
        await ctx.send(embed=message)

    @commands.command(name="say")
    async def say_something(self, ctx: commands.Context, *, args: str) -> None:
        """Make the bot say something for you.

        Args:
            ctx (commands.Context): The context.
            arg (str): The thing to say.
        """

        await ctx.send(f"{args}")

    @commands.command(name="rand")
    async def rand(self, ctx: commands.Context, number: int = 6) -> None:
        """Select a random number between a range and say it to the channel.

        Args:
            ctx (commands.Context): The context.
            number (int): The range.
        """

        message: discord.Embed = EmbedCreator.create_embed(
            name=f"Rand",
            value=f"{ctx.author.mention} Rand of **{number}**. "
            f"Result: **{random.randint(1, number)}**",
        )
        await ctx.send(embed=message)

    @commands.command(name="choice")
    async def choice(self, ctx: commands.Context, *choices) -> None:
        """Select a random choices between a list of choices and output to the channel.

        Args:
            ctx (commands.Context): The context.
            choices (list[str]): The list of choices.
        """
        message: discord.Embed
        try:
            message = EmbedCreator.create_embed(
                name=f"Choices between : {', '.join(choices)}",
                value=f"{ctx.author.mention} The **choice** is: "
                f"**{random.choice(choices)}**",
            )
        except IndexError:
            message = EmbedCreator.create_embed(
                name=f"No arguments",
                value=f"You need to give arguments so i can choose !",
            )
        finally:
            await ctx.send(embed=message)

    @commands.command(name="ask")
    async def ask(self, ctx: commands.Context, *, question) -> None:
        """Make the bot answer a question."""

        choices: list[str] = [
            "Yes",
            "No",
            "Maybe",
            "Dunno",
            "Clearly",
            "Definitely",
            "Without a doubt",
            "I don't think so",
            "I rather not answer that, weirdo",
        ]

        message: discord.Embed = EmbedCreator.create_embed(
            name=f" Question : {question}",
            value=f"{ctx.author.mention} | **{random.choice(choices)}**.",
        )
        await ctx.send(embed=message)
