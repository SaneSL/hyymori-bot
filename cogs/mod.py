import discord
from discord.ext import commands

from cogs.utils.db import remove_command_from_db


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['rem'])
    async def remove_command(self, ctx, name):
        removed = self.bot.remove_command(name)

        remove_command_from_db(ctx, name)

        await ctx.send(f"Poistettiin komento: {name}")

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author) or ctx.author.id in self.bot.whitelist


def setup(bot):
    bot.add_cog(Mod(bot))