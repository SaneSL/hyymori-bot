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




    def add_custom_command(self, ctx, name):

        # Check for attachments
        

        @commands.command(name=name)
        async def cmd(ctx):
            await ctx.send("Tämä mämmi")

        return cmd  

    async def get_context(self, message):
        ctx = await super().get_context(message)

        # Try to add command if there isn't one
        if ctx.command is None:
            ctx.command = self.add_custom_command(ctx, name=ctx.invoked_with)


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
    # commands = bot.commands

    # for command in commands:
    #     print(command.name)

    bot.run(cfg['token'])


run_bot()