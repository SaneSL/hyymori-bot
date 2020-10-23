import discord

from discord.ext import commands
from pathlib import Path
from cogs.utils.db import get_command



# Add image support

def create_text_command(name, content):
        @commands.command(name=name)
        async def cmd(ctx):
            await ctx.send(content)

        return cmd, 'text'


def create_audio_command(ctx, name, audio_fn):
        @commands.command(name=name)
        async def cmd(ctx):
            # Invoker not in voice
            if ctx.author.voice is None:
                return

            channel = ctx.author.voice.channel

            # Bot not in voice
            if ctx.voice_client is None:
                await channel.connect()
            else:
                await ctx.voice_client.move_to(channel)

            audio_fp = f"cogs/audio/{audio_fn}"
            audio_source = discord.FFmpegPCMAudio(audio_fp)
            ctx.voice_client.play(audio_source)

        return cmd, 'audio'


async def re_add_custom_command(ctx):
    name = ctx.invoked_with
    
    # Get data from db
    res = get_command(ctx)

    # None handled in process_commands
    if res is None:
        return

    cmd = res[0]['command']
    output = cmd['output']
    cmd_type = cmd['type']

    if cmd_type == 'text':
        cmd, cmd_type = create_text_command(name, output)

        # Add command to bot
        ctx.bot.add_command(cmd)

        return cmd

    elif cmd_type == 'audio':
        cmd, cmd_type = create_audio_command(ctx, name, output)
        
        # Add command to bot
        ctx.bot.add_command(cmd)

        return cmd


async def create_custom_command(ctx, name, output=None):
    # Check for attachments
    attachments = ctx.message.attachments
    content = output or ctx.message.content

    # Text command
    if len(attachments) == 0 and content:
        cmd, cmd_type = create_text_command(name, output)
        return cmd, (cmd_type, None)

    if len(attachments) == 1:
        # Check file type, only mp3 allowed
        audio_fn = attachments[0].filename
        if not audio_fn.endswith('.mp3'):
            return await ctx.send("Vain .mp3 liitteet sallittu")

        # Make new name based on command name for the file. Only .mp3
        audio_fn = name + ".mp3"

        # Save file
        new_fp = Path(__file__).parent.parent.absolute().joinpath('audio', audio_fn)
        await attachments[0].save(new_fp)

        cmd, cmd_type = create_audio_command(ctx, name, audio_fn)

        # Create new tuple to add fn
        return cmd, (cmd_type, audio_fn)

    else:
        await ctx.send("Lisää max 1 liite tai joku muu virhe")
        return False, False