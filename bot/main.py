from discord.ext import commands
import dotenv
import os
import discord
from cogs.music_cog import MusicCog
from cogs.admin_cog import AdminCog
from cogs.user_cog import UserCog
from cogs.utils_cog import UtilsCog
from cogs.event_cog import EventCog

dotenv.load_dotenv()

intents: discord.Intents = discord.Intents.default()
intents.members = True
client: commands.Bot = commands.Bot(
    command_prefix="!", intents=intents, help_command=None
)
cogs: list[commands.Cog] = [AdminCog, UserCog, UtilsCog, MusicCog, EventCog]


for cog in cogs:
    client.add_cog(cog(client))

client.run(os.getenv("TOKEN"))
