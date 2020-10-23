import discord
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # async def cmd(self, ctx):
    #     # Invoker not in voice
    #     if ctx.author.voice is None:
    #         return

    #     channel = ctx.author.voice.channel

    #     # Bot not in voice
    #     if ctx.voice_client is None:
    #         await channel.connect(reconnect=True)
    #     else:
    #         await ctx.voice_client.move_to(channel)

    #     audio_fp = f"cogs/audio/maisa.mp3"
    #     audio_source = discord.FFmpegPCMAudio(audio_fp)
    #     ctx.voice_client.play(audio_source)


def setup(bot):
    bot.add_cog(Misc(bot))