import discord
from discord.ext import commands

from cogs.utils.add_command import create_custom_command


class CustomCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #def check_attachment_type():
        

    _custom_commands = {}

    @commands.command()
    async def add_command(self, ctx, name, *, output=None):
        print(output)
        existing_command = self._custom_commands.get(name)

        # Don't allow overriding build ins
        if existing_command is None and ctx.bot.get_command(name):
            return await ctx.send(f"Tätä nimeä ei voi käyttää")

        # Overwrite old command
        if existing_command:
            self._custom_commands[name][ctx.guild.id] = output
            
        else:
            cmd = await create_custom_command(ctx, name, output)

            # This stuff might be usefull if all commands are under this
            # cmd.cog = self
            # And add it to the cog and the bot
            # self.__cog_commands__ = self.__cog_commands__ + (cmd,)

            ctx.bot.add_command(cmd)
            # Now add it to our list of custom commands
            self._custom_commands[name] = {ctx.guild.id: output}

        await ctx.send(f"Added a command called {name}")


    # @commands.command()
    # async def add(self, ctx):
    #     attachments = ctx.message.attachments

    #     if len(attachments) != 1:
    #         return await ctx.send("Lisää max 1 liite")

        



def setup(bot):
    bot.add_cog(CustomCommands(bot))