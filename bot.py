import os
import discord
import json

from discord.ext import commands


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
                self.load_extension(f"cogs.{name}")



def run_bot():
    cfg = get_cfg()

    bot = Huumori(command_prefix=cfg['prefix'])
    bot.run(cfg['token'])


run_bot()