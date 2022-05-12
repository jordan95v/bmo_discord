import discord


class EmbedMaker:
    """Used to make embed message to stay DRY."""

    @classmethod
    def make_embed(cls, name: str, value: str) -> discord.Embed:
        message: discord.Embed = discord.Embed(color=discord.Color.purple())
        message.add_field(name=name, value=value)
        return message
