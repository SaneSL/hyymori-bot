import discord
from discord.ext import commands

from cogs.utils.db import add_to_db_whitelist, remove_from_db_whitelist


class Admin(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wl_add(self, ctx, member: discord.Member):
        if member.id == self.bot.user.id or member.id is None:
            return

        add_to_db_whitelist(member.id)
        
    @commands.command()
    async def wl_remove(self, ctx, member: discord.Member):
        if member.id == self.bot.user.id or member.id is None:
            return

        remove_from_db_whitelist(member.id)

    @commands.command()
    async def cc(self, ctx):
        commands = self.bot.commands
        for command in commands:
            print(command.name)

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)


def setup(bot):
    bot.add_cog(Admin(bot))
