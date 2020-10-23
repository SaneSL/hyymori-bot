import os
import discord
import json

from discord.ext import commands
from cogs.utils.add_command import re_add_custom_command
from cogs.utils.db import command_exists, load_whitelist


def get_cfg():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    with open('config.json') as json_data_file:
        cfg = json.load(json_data_file)
    return cfg


class Huumori(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Load cogs
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                name = filename[:-3]
                if name == 'music':
                    continue
                self.load_extension(f"cogs.{name}")

    async def get_context(self, message):
        ctx = await super().get_context(message)

        # Try to add command
        if ctx.command is None and command_exists(ctx):
            ctx.command = await re_add_custom_command(ctx)

        return ctx

    async def process_commands(self, message):
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


def run_bot():
    cfg = get_cfg()

    bot = Huumori(command_prefix=cfg['prefix'])
    
    bot.whitelist = load_whitelist()

    bot.run(cfg['token'])


run_bot()