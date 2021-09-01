# Importing Modules
import discord
# import async_tio
from cogs.ext.tio import Tio
from discord.ext import commands


class Compiler(commands.Cog):
    """ Cog class for compiler commands """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.site = Tio()

    @commands.command(name="compile", aliases=["run"])
    async def compile(self, ctx, *, code):
        request = self.site.new_request('python3', code)
        result = self.site.send(request).split('\n')
        output = "\n".join(result[:-6]).replace('.code.tio', 'main.py')
        status = result[-1]
        await ctx.send(f"```yaml\n{output}\n\n{status}```")

# Setting up cog


def setup(bot):
    bot.add_cog(Compiler(bot))
