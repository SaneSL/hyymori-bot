import os
import discord
import json
import logging

from discord.ext import commands
from cogs.utils.command_factory import re_add_custom_command
from cogs.utils.db import command_exists, load_whitelist, incr_command_count, get_random_command_name_from_db
from cogs.utils.customhelp import CustomHelpCommand

"""
TODO:

"""

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


def get_cfg():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    with open('config.json') as json_data_file:
        cfg = json.load(json_data_file)
    return cfg


class Huumori(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.log = logger
        
        # Load cogs
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                name = filename[:-3]
                if name in ('events'):
                    continue
                self.load_extension(f"cogs.{name}")

    async def get_context(self, message):
        ctx = await super().get_context(message)

        # Try to add command
        if ctx.command is None and command_exists(ctx, ctx.invoked_with):
            ctx.command = await re_add_custom_command(ctx)

        return ctx

    async def process_commands(self, message):
        if message.content == '!random':
            r = get_random_command_name_from_db()
            message.content = '!' + r

        ctx = await self.get_context(message)
        author_id = message.author.id

        # Allow commands only in guild
        if ctx.guild is None:
            return

        # Don't allow bot to invoke commands
        if message.author.bot:
            return

        if ctx.command is None:
            return

        await self.invoke(ctx)

        incr_command_count(ctx, ctx.command.name)


def run_bot():
    cfg = get_cfg()

    bot = Huumori(command_prefix=cfg['prefix'], help_command=CustomHelpCommand(prefixes=cfg['prefix']))
    
    bot.whitelist = load_whitelist()

    bot.run(cfg['token'])


run_bot()