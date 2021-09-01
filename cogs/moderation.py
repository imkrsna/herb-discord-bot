# Importing Modules
import discord
from discord.ext import commands


class Moderation(commands.Cog):
    """ Cog class for moderation commands """

    def __init__(self, bot: commands.Bot):
        self.bot = bot


# Setting up cog
def setup(bot):
    bot.add_cog(Moderation(bot))
