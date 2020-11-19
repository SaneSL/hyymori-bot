import discord
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ohjeet(self, ctx):
        await ctx.send(file=discord.File('ohjeet.png'))


def setup(bot):
    bot.add_cog(Misc(bot))