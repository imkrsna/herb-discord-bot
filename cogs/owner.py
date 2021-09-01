# Importing Modules
import os
import discord
import functools
from discord.ext import commands
from difflib import get_close_matches


class Owner(commands.Cog):
    """ Cog class for bot owner/me """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # example of async custom decorator
    def auto_react():
        def wrapper(func):
            @functools.wraps(func)
            async def wrapped(*args, **kwargs):
                msg = await func(*args, **kwargs)
                await msg.add_reaction("<:on:882286109063782410>")
            return wrapped
        return wrapper

    ### LOAD COGS ###
    @commands.command(name="load", aliases=["loadcog"])
    @commands.is_owner()
    @auto_react()
    async def loadcog(self, ctx, *, cog: str):
        try:
            self.bot.load_extension(f"cogs.{cog.lower()}")
            embed = discord.Embed(
                title="Loaded!", description=f"```yaml\n- '{cog}' loaded.```")
            return await ctx.send(embed=embed)

        except commands.errors.ExtensionAlreadyLoaded:
            embed = discord.Embed(
                title="Already Loaded!", description=f"```diff\n- '{cog}' already loaded.```", color=self.bot.theme_color)
            return await ctx.send(embed=embed)

        except commands.errors.ExtensionNotFound:
            # getting all extension
            extensions = [filename[:-3]
                          for filename in os.listdir('./cogs') if filename.endswith('.py')]
            # getting all matches
            matches = get_close_matches('cogs.' + cog, extensions)

            # if match found
            if len(matches) > 0:
                notfound = f"```diff\n- '{cog}' not found.```"
                didyoumean = f"**Did You Mean:**```yaml\n- '{matches[0]}'```"

                embed = discord.Embed(
                    title="Not Found!", description=f"{notfound}\n{didyoumean}", color=self.bot.theme_color)
            # if match not found
            else:
                notfound = f"```diff\n- '{cog}' not found.```"
                embed = discord.Embed(
                    title="Not Found!", description=f"{notfound}", color=self.bot.theme_color)

            return await ctx.send(embed=embed)

    ### UNLOAD COGS ###
    @commands.command(name="unload", aliases=["unloadcog"])
    @commands.is_owner()
    @auto_react()
    async def unloadcog(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(f"cogs.{cog.lower()}")
            embed = discord.Embed(
                title="Unloaded!", description=f"```yaml\n- '{cog}' unloaded.```", color=self.bot.theme_color)
            return await ctx.send(embed=embed)

        except commands.errors.ExtensionNotLoaded:
            embed = discord.Embed(
                title="Not Loaded!", description=f"```diff\n- '{cog}' not loaded.```", color=self.bot.theme_color)
            return await ctx.send(embed=embed)

    ### RELOAD COGS ###
    @commands.command(name="reload", aliases=["reloadcog"])
    @commands.is_owner()
    @auto_react()
    async def reloadcog(self, ctx, *, cog: str):
        try:
            self.bot.reload_extension(f"cogs.{cog.lower()}")
            embed = discord.Embed(
                title="Reloaded!", description=f"```yaml\n- '{cog}' reloaded.```", color=self.bot.theme_color)
            return await ctx.send(embed=embed)

        except commands.errors.ExtensionNotLoaded:
            embed = discord.Embed(
                title="Not Loaded!", description=f"```diff\n- '{cog}' not loaded.```", color=self.bot.theme_color)
            return await ctx.send(embed=embed)

    ### CLS ###
    @commands.command(name="cls")
    @commands.is_owner()
    async def cls(self, ctx):
        clear = 'cls' if os.name == 'nt' else 'clear'
        _ = os.system(clear)

    @commands.command(name='cogs')
    @commands.is_owner()
    @auto_react()
    async def get_cogs(self, ctx):
        # getting all loaded cogs
        loaded = [key for key in self.bot.cogs.keys()]
        # getting all cogs
        cogs = [filename[:-3]
                for filename in os.listdir('./cogs') if filename.endswith('.py')]
        max_len = len(max(cogs, key=len)) + 16

        # creating embed, calculating number of space relative to longest
        description = "```yaml\n- All avilable cogs```\n"
        for cog in cogs:
            if cog.capitalize() in loaded:
                description += f"`{cog.capitalize()}{(max_len - len(cog))*' '}`<:on:882286109063782410> \n"
            else:
                description += f"`{cog.capitalize()}{(max_len - len(cog))*' '}`<:off:882286108350750721>\n"

        embed = discord.Embed(
            title="Cogs", description=description, color=self.bot.theme_color)
        msg = await ctx.send(embed=embed)
        return msg


# Setting up cog
def setup(bot):
    bot.add_cog(Owner(bot))
