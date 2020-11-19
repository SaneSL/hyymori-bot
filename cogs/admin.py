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

        self.bot.whitelist.append(member.id)

        add_to_db_whitelist(member.id)

        await ctx.message.delete(delay=5)
        await ctx.send("Oikat annettu", delete_after=5)
        
    @commands.command()
    async def wl_remove(self, ctx, member: discord.Member):
        if member.id == self.bot.user.id or member.id is None:
            return

        self.bot.whitelist = [x for x in self.bot.whitelist if x != member.id]

        remove_from_db_whitelist(member.id)

        await ctx.message.delete(delay=5)
        await ctx.send("Oikat poistettu", delete_after=5)

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)


def setup(bot):
    bot.add_cog(Admin(bot))
