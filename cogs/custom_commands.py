import discord
from discord.ext import commands

from cogs.utils.command_factory import create_custom_command
from cogs.utils.db import command_exists, add_command_to_db


class CustomCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add_command(self, ctx, name, *, output=None):
        if len(name) > 20:
            await ctx.send('Komennon pituus max 20 merkkiä')

        cmd_exists = command_exists(ctx, name)

        if cmd_exists:
            return await ctx.send("Komennon nimi on jo käytössä")

        # Don't allow overriding build ins
        if ctx.bot.get_command(name):
            return await ctx.send("Tätä nimeä ei voi käyttää")

        # Overwrite old command - not done
            
        else:
            cmd, cmd_tuple = await create_custom_command(ctx, name, output)
            
            # Error in creating
            if not cmd:
                return

            # Switch output for filename for audio files
            if cmd_tuple[0] in ('audio', 'image'):
                output = cmd_tuple[1]
            
            # Bad implementation
            cmd_type = cmd_tuple[0]
            
            # This stuff might be usefull if all commands are under this
            # cmd.cog = self
            # And add it to the cog and the bot
            # self.__cog_commands__ = self.__cog_commands__ + (cmd,)

            # Add command
            ctx.bot.add_command(cmd)
            add_command_to_db(ctx.guild.id, name, output, cmd_type, ctx.author.display_name)

        await ctx.send(f"Lisättiin komento: {name}")
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(CustomCommands(bot))