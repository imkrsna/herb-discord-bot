# Importing Modules
import os
import discord
from difflib import get_close_matches
from discord.ext import commands


class Errorhandeler(commands.Cog):
    """ Error Handeling """

    def __init__(self, bot):
        self.bot = bot

    ### EVENTS ###
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.NotOwner):
            pass

        elif isinstance(error, commands.errors.CommandNotFound):
            # getting inoked command ie the command that cause error
            cmd = ctx.invoked_with
            # getting all commands
            cmds = [cmd.name for cmd in self.bot.commands]
            # getting all matches
            matches = get_close_matches(cmd, cmds)

            # creting embed if any match found
            if len(matches) > 0:
                notfound = f"```diff\n- '{cmd}' not found!```"
                didyoumean = f"**Did You Mean:**```yaml\n- '{matches[0]}'```"

                embed = discord.Embed(
                    title="Command Not Found!", description=f"{notfound}\n{didyoumean}")
                await ctx.send(embed=embed)
        
        else:
            raise(error)


# Setting up cog
def setup(bot):
    bot.add_cog(Errorhandeler(bot))
