import discord


class EmbedCreator:
    """Used to make embed message to stay DRY."""

    @classmethod
    def create_embed(cls, name: str, value: str) -> discord.Embed:
        """Create an discord embed message.

        Args:
            name (str): Name of the message.
            value (str): Value of the message.

        Returns:
            discord.Embed: The message.
        """

        message: discord.Embed = discord.Embed(color=discord.Color.purple())
        message.add_field(name=name, value=value)
        return message
