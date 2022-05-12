from discord.ext import commands
import discord
from utils.embed_maker import EmbedMaker


class UserCog(commands.Cog):
    """Contains sevral usefull (or not) user related commands."""

    def __init__(self, client: commands.Bot) -> None:
        """Constructor"""

        self.client: commands.Bot = client

    @commands.command(name="old")
    async def how_old(self, ctx: commands.Context) -> None:
        """Say from which date a member is on this server.

        Args:
            ctx (commands.Context): The context.
        """
        date = ctx.message.author.joined_at.strftime("%d %B %Y")
        message: discord.Embed = EmbedMaker.make_embed(
            name=f"How old are you here ?",
            value=f"{ctx.author.mention} is here since **{date}** !",
        )
        await ctx.send(embed=message)

    @commands.command(name="nick")
    @commands.has_permissions(manage_nicknames=True)
    async def change_nick(
        self, ctx: commands.Context, member: discord.Member, nick: str
    ) -> None:
        """Change the nickname of a user.

        Args:
            ctx (commands.Context): The context.
            member (discord.Member): The user to change the nickname.
            nick (str): The new nickname.
        """

        message: discord.Embed
        old_name: str = member.nick
        try:
            if member is ctx.guild.me:
                message = EmbedMaker.make_embed(
                    name=f"Permission error.",
                    value=f"You have no permission to change my name !",
                )
                await ctx.send(embed=message)
                return
            await member.edit(nick=nick)
        except discord.errors.Forbidden:
            message = EmbedMaker.make_embed(
                name=f"Permission error.",
                value=f"You have no permission to change **{member.nick}'s** nickname !",
            )
            await ctx.send(embed=message)
        else:
            message = EmbedMaker.make_embed(
                name=f"Rename is a success.",
                value=f"{ctx.author.mention} changed **{old_name}** nickname to **{nick}** !",
            )
            await ctx.send(embed=message)
