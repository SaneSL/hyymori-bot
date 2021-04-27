import discord

from cogs.utils.db import get_all_commands_from_db, get_command_from_db, get_random_command_name_from_db, get_top_x_commands_from_db, remove_entry_from_db, upsert_to_entry
from pydub import AudioSegment
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ohjeet(self, ctx):
        await ctx.send(file=discord.File('ohjeet.png'))

    @commands.command()
    async def random(self, ctx):
        return

        # r_command_name = get_random_command_name_from_db(ctx.guild.id)

        # msg = ctx.message

        # ctx.

        # await self.bot.process_commands()
    
    @commands.command()
    async def top(self, ctx):
        name_count_pairs = get_top_x_commands_from_db(ctx.guild.id)

        embed = discord.Embed(
            title="Top 7",
            colour=discord.Colour.dark_magenta()
        )

        cmd_string = ""

        for p in name_count_pairs:
            name = p[0]
            count = p[1]

            f = str(name) + ":" + str(count) + "\n"

            cmd_string += f

        embed.add_field(name='Commands', value=cmd_string)

        await ctx.send(embed=embed)


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

    @commands.command()
    async def add_entry(self, ctx, command_name):
        r = upsert_to_entry(ctx.author, command_name)

        if r is False:
            await ctx.send("Tämän nimistä komentoa ei ole olemassa.")
        else:
            await ctx.send("Entry lisätty!")

    @commands.command(aliases=['rm_entry'])
    async def remove_entry(self, ctx):
        remove_entry_from_db(ctx.author)

        await ctx.send("Poistettiin entry!")


def setup(bot):
    bot.add_cog(Misc(bot))