import discord
from discord.ext import commands
from cogs.utils.db import get_all_commands_from_db


class CustomHelpCommand(commands.DefaultHelpCommand):
    def __init__(self, **kwargs):
        super().__init__(verify_checks=False, command_attrs={"hidden": True})
        self.prefixes = ", ".join(kwargs.pop('prefixes'))

    async def send_command_help(self, command):
        # Fixes help command subclassing issue with custom command
        if command.name == 'help':
            return

        dest = self.get_destination()

        if command.cog is None:
            await dest.send('Ei apuu...')
            return

        embed = discord.Embed(
            title='Command: ' + command.name,
            colour=discord.Colour.gold()
        )

        if command.description:
            desc = command.description
        else:
            desc = "-"

        if command.aliases:
            aliases = "\n".join(command.aliases)
        else:
            aliases = "-"

        if command.signature:
            usage_value = '!' + command.name + ' ' + command.signature + '\n [] parameters are optional.\n' \
                                                                         'If you want to give a parameter with spaces' \
                                                                         ' use quotation marks `""`'
        else:
            usage_value = '!' + command.name

        embed.description = desc
        embed.add_field(name='Aliases', value=aliases, inline=True)
        embed.add_field(name='Usage', value=usage_value, inline=False)

        await dest.send(embed=embed)

    async def send_cog_help(self, cog):
        return

    async def send_bot_help(self, mapping):
        """
        Sends embed with a list of all commands and other info to invokers channel
        Parameters
        ----------
        mapping
            Dict with Cogs and their Commands
        """
        dest = self.get_destination()

        custom_cmd_list = get_all_commands_from_db(dest.guild.id)
        to_ignore = ('Admin', 'CommandErrorHandler')
        embed = discord.Embed(
            title="Komennot",
            colour=discord.Colour.dark_magenta()
        )

        # Add internal commands
        for cog, cog_commands in mapping.items():
            name = cog.qualified_name if cog is not None else None
            if name in to_ignore or name is None:
                continue
            sorted_commands = await self.filter_commands(cog_commands, sort=True)
            if sorted_commands:
                cmd_list = []
                for cmd in sorted_commands:
                    cmd_name = str(cmd)
                    cmd_list.append(cmd_name)

                cmd_string = '\n'.join(cmd_list)
                embed.add_field(name=name, value=cmd_string)

        if custom_cmd_list:
            # Add user made commands
            i = 1

            custom_cmd_string = ''
            for cmd in custom_cmd_list:
                # Skip separator for last command
                if i == len(custom_cmd_list):
                    custom_cmd_string += cmd
                # 4 commands per row
                elif i % 4 == 0:
                    custom_cmd_string += cmd + '\n'
                # Command separator
                else:
                    custom_cmd_string += cmd + '   ---   '
                i += 1
            
            embed.add_field(name='User made', value=custom_cmd_string, inline=False)

        embed.add_field(name='Prefixe(s)', value=self.prefixes, inline=False)

        await dest.send(embed=embed)
