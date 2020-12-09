import discord

from cogs.utils.db import get_command_from_db
from pydub import AudioSegment
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ohjeet(self, ctx):
        await ctx.send(file=discord.File('ohjeet.png'))

    @commands.command()
    async def editvol(self, ctx, cmd_name, db):
        db = int(db)
        
        cmd_name = cmd_name.lower()

        if db <= -50 or db >= 50:
            return await ctx.send("Max väli 50")

        res = get_command_from_db(ctx.guild.id, cmd_name)

        if res is None:
            return await ctx.send("Tämän nimistä komentoa ei ole olemassa.")

        cmd_type = res[0]['command']['type']

        if cmd_type != 'audio':
            return await ctx.send("Tämä komento ei ole ääni-komento.")

        audio_fn = f"cogs/audio/{cmd_name}.mp3"

        audio_f = AudioSegment.from_mp3(audio_fn)

        new_audio = audio_f + db

        new_audio.export(audio_fn)

        msg = f"{cmd_name} {str(db)} dB"

        await ctx.send(msg, delete_after=5)
        

def setup(bot):
    bot.add_cog(Misc(bot))