import discord
from discord.ext import commands


async def create_custom_command(ctx, name, output=None):

    # Check for attachments
    attachments = ctx.message.attachments
    content = output or ctx.message.content

    # Text command
    if len(attachments) == 0 and content:
        print("text")
        @commands.command(name=name)
        async def cmd(ctx):
            await ctx.send(content)

        return cmd


    if len(attachments) == 1:
        # Check file type, only mp3 allowed
        audio_fn = attachments[0].filename
        if not audio_fn.endswith('.mp3'):
            return await ctx.send("Vain .mp3 liitteet sallittu")

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

        return cmd

    else:
        return await ctx.send("Lisää max 1 liite")
    

    @commands.command(name=name)
    async def cmd(ctx):
        await ctx.send("Tämä mämmi")

    return cmd  