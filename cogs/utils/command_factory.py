import discord
import asyncio

from discord.ext import commands
from pathlib import Path

from cogs.utils.db import get_command_from_db
from cogs.utils.cmd import CommandData


def create_text_command(name, content):
        @commands.command(name=name)
        async def cmd(ctx):
            await ctx.send(content)

        return CommandData(cmd=cmd, ctype='text')


def create_image_command(ctx, name, image_fn):
    @commands.command(name=name)
    async def cmd(ctx):
        image_fp = f"cogs/image/{image_fn}"
        await ctx.send(file=discord.File(image_fp))
    

    return CommandData(cmd=cmd, ctype='image')


def create_audio_command(ctx, name, audio_fn):
        @commands.command(name=name)
        async def cmd(ctx):
            # Invoker not in voice
            if ctx.author.voice is None:
                await ctx.send("Ääni komento. Sun pitää olla kannulla bro", delete_after=5)
                return

            channel = ctx.author.voice.channel
            vc = ctx.voice_client

            if vc:
                # Bot is not in invokers channel
                if vc.channel.id != channel.id:
                    try:
                        # await vc.move_to(channel)
                        await vc.disconnect()
                        await channel.connect()

                    except asyncio.TimeoutError:
                        raise VoiceConnectionError(f'Moving to channel: <{channel}> timed out.')
            else:
                try:
                    await channel.connect()
                except asyncio.TimeoutError:
                    raise VoiceConnectionError(f'Connecting to channel: <{channel}> timed out.')
            
            # If playing, move to other channel, but don't play anything
            if ctx.voice_client.is_playing():
                return

            audio_fp = f"cogs/audio/{audio_fn}"
            audio_source = discord.FFmpegPCMAudio(audio_fp)
            ctx.voice_client.play(audio_source)

        return CommandData(cmd=cmd, ctype='audio')


async def re_add_custom_command(ctx):
    name = ctx.invoked_with
    
    # Get data from db
    res = get_command_from_db(ctx.guild.id, name)

    # None handled in process_commands
    if res is None:
        return

    output = res[0]['command']['output']
    cmd_type = res[0]['command']['type']

    if cmd_type == 'text':
        cmd_data = create_text_command(name, output)

        # Add command to bot
        ctx.bot.add_command(cmd_data.cmd)

        return cmd_data.cmd

    elif cmd_type == 'audio':
        cmd_data = create_audio_command(ctx, name, output)
        
        # Add command to bot
        ctx.bot.add_command(cmd_data.cmd)

        return cmd_data.cmd

    elif cmd_type == 'image':
        cmd_data = create_image_command(ctx, name, output)

        # Add command to bot
        ctx.bot.add_command(cmd_data.cmd)

        return cmd_data.cmd


async def create_custom_command(ctx, name, output=None):
    # Check for attachments
    attachments = ctx.message.attachments
    content = output or ctx.message.content

    # Text command
    if len(attachments) == 0 and output:
        cmd_data = create_text_command(name, output)
        return cmd_data

    if len(attachments) == 1:
        # Check for too big attachements, bytes
        if attachments[0].size > 1000000:
            return await ctx.send('Liian iso liite, max 1000 KB')

        # Create new name for the file based on command name
        fn = attachments[0].filename
        suffix = Path(fn).suffix
        new_fn = (name + suffix).lower()

        is_img = fn.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))

        if is_img:
            cmd_data = create_image_command(ctx, name, new_fn)

            # Save file
            new_fp = Path(__file__).parent.parent.absolute().joinpath('image', new_fn)
            await attachments[0].save(new_fp)

            cmd_data.output = new_fn

            return cmd_data
        else:
            # Check file type, only mp3 allowed
            if suffix not in ('.mp3'):
                return await ctx.send("Vain .mp3 liitteet sallittu")

            # Save file
            new_fp = Path(__file__).parent.parent.absolute().joinpath('audio', new_fn)
            await attachments[0].save(new_fp)

            cmd_data = create_audio_command(ctx, name, new_fn)

            cmd_data.output = new_fn
            return cmd_data

    else:
        await ctx.send("Lisää max 1 liite tai joku muu virhe")
        return None