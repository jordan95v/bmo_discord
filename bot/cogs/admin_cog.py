from discord.ext import commands
import discord
import dotenv
from utils.embed_maker import EmbedMaker


class AdminCog(commands.Cog):
    """'Contains commands for administator."""

    def __init__(self, client: commands.Bot) -> None:
        """Constructor"""

        self.client: commands.Bot = client
        dotenv.load_dotenv()

    @commands.command(name="del")
    @commands.has_permissions(manage_messages=True)
    async def delete_messages(self, ctx: commands.Context, number: int) -> None:
        """Delete message from a discord channel.

        Args:
            ctx (commands.Context): The context.
            number (int): The number of message to delete.
        """

        message: discord.Embed
        if number > 50:
            message = EmbedMaker.make_embed(
                name=f"Error for delete",
                value=f"You cannot delete that number of messages, limit is 50.",
            )
            await ctx.send(embed=message)
            return

        messages = await ctx.channel.purge(limit=number + 1)
        message = EmbedMaker.make_embed(
            name=f"Delete",
            value=f"Deleted **{len(messages)- 1}** message{'s' if len(messages) > 2 else ''} !",
        )
        await ctx.send(embed=message)

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(
        self, ctx: commands.Context, member: discord.Member, *, reason=None
    ) -> None:
        """Kicks a member from the server.

        Args:
            ctx (commands.Context): The context.
            member (discord.Member): The member to kick.
            reason (str): The reason of the kick.
        """

        message: discord.Embed = EmbedMaker.make_embed(
            name=f"Kick",
            value=f"{member.mention} have been kicked by {ctx.author.mention}, reason : **{reason}**",
        )
        await member.kick(reason=reason)
        await ctx.send(embed=message)

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(
        self, ctx: commands.Context, member: discord.Member, *, reason=None
    ) -> None:
        """Bans a member from the server.

        Args:
            ctx (commands.Context): The context.
            member (discord.Member): The member to ban.
            reason (str): The reason of the ban.
        """

        message: discord.Embed = EmbedMaker.make_embed(
            name=f"Ban",
            value=f"{member.mention} have been banned by {ctx.author.mention}, reason : **{reason}**",
        )
        await member.ban(reason=reason)
        await ctx.send(embed=message)

    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx: commands.Context, *, member) -> None:
        """Unban a member from the server.

        Args:
            ctx (commands.Context): The context.
            member (str): The member to unban.
        """

        banned_users: list[discord.guild.BanEntry] = await ctx.guild.bans()
        message: discord.Embed
        try:

            user_name, user_discriminator = member.split("#")
        except ValueError:
            message = EmbedMaker.make_embed(
                name=f"Ban",
                value=f"Make sure you spelled the nam ecorrectly -> xxx#1234",
            )
            await ctx.send(embed=message)
        else:
            for ban_entry in banned_users:
                user: discord.Member = ban_entry.user

                if (user.display_name, user.discriminator) == (
                    user_name,
                    user_discriminator,
                ):
                    await ctx.guild.unban(user)
                    message = EmbedMaker.make_embed(
                        name=f"Ban",
                        value=f"{ctx.author.mention} unbanned {user.mention}.",
                    )
                    await ctx.send(embed=message)
                    return

            message = EmbedMaker.make_embed(
                name=f"Ban",
                value=f"{member} cannot be unbanned.",
            )
            await ctx.send(embed=message)
