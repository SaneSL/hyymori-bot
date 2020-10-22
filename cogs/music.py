import discord
from discord.ext import commands


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel

        await channel.connect()

        # if ctx.voice_client is not None:
        #     return await ctx.voice_client.move_to(channel)
    

    @commands.command()
    async def play(self, ctx):
        audio_source = discord.FFmpegPCMAudio('cogs/maisa.mp3')
        ctx.voice_client.play(audio_source)

        await ctx.send("Now playing maisa.mp3")


def setup(bot):
    bot.add_cog(Music(bot))