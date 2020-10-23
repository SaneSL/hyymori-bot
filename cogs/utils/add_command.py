import discord

from discord.ext import commands
from pathlib import Path
from cogs.utils.db import get_command_from_db


def create_text_command(name, content):
        @commands.command(name=name)
        async def cmd(ctx):
            await ctx.send(content)

        return cmd, 'text'


def create_image_command(ctx, name, image_fn):
    @commands.command(name=name)
    async def cmd(ctx):
        image_fp = f"cogs/image/{image_fn}"
        await ctx.send(file=discord.File(image_fp))
    
    return cmd, 'image'


def create_audio_command(ctx, name, audio_fn):
        @commands.command(name=name)
        async def cmd(ctx):
            # Invoker not in voice
            if ctx.author.voice is None:
                return

            channel = ctx.author.voice.channel

            # Bot not in voice
            if ctx.voice_client is None:
                await channel.connect(reconnect=True)
            else:
                await ctx.voice_client.move_to(channel)


            audio_fp = f"cogs/audio/{audio_fn}"
            audio_source = discord.FFmpegPCMAudio(audio_fp)
            ctx.voice_client.play(audio_source)

        return cmd, 'audio'


async def re_add_custom_command(ctx):
    name = ctx.invoked_with
    
    # Get data from db
    res = get_command_from_db(ctx.guild.id, name)

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

    elif cmd_type == 'image':
        cmd, cmd_type = create_image_command(ctx, name, output)

        # Add command to bot
        ctx.bot.add_command(cmd)

        return cmd


async def create_custom_command(ctx, name, output=None):
    # Check for attachments
    attachments = ctx.message.attachments
    content = output or ctx.message.content

    # Text command
    if len(attachments) == 0 and output:
        cmd, cmd_type = create_text_command(name, output)
        return cmd, (cmd_type, None)

    if len(attachments) == 1:
        fn = attachments[0].filename
        suffix = Path(fn).suffix
        new_fn = (name + suffix).lower()

        is_img = fn.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))
        if is_img:
            cmd, cmd_type = create_image_command(ctx, name, new_fn)

            # Save file
            new_fp = Path(__file__).parent.parent.absolute().joinpath('image', new_fn)
            await attachments[0].save(new_fp)

            return cmd, (cmd_type, new_fn)
        else:
            fn = attachments[0].filename
            suffix = Path(fn).suffix
            new_fn = (name + suffix).lower()

            # Check file type, only mp3 allowed
            if suffix not in ('.mp3'):
                return await ctx.send("Vain .mp3 liitteet sallittu")

            # Save file
            new_fp = Path(__file__).parent.parent.absolute().joinpath('audio', new_fn)
            await attachments[0].save(new_fp)

            cmd, cmd_type = create_audio_command(ctx, name, new_fn)

            # Create new tuple to add fn
            return cmd, (cmd_type, new_fn)

    else:
        await ctx.send("Lisää max 1 liite tai joku muu virhe")
        return False, False