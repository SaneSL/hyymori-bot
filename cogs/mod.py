import discord
from discord.ext import commands



class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author) or ctx.author.id in self.bot.whitelist


def setup(bot):
    bot.add_cog(Mod(bot))