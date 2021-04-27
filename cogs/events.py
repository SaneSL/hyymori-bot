from cogs.utils.db import get_entry_from_db
from cogs.utils.errors import VoiceConnectionError
import discord
from discord.ext import commands
from datetime import date, datetime
import asyncio


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.entries = {}

    def allow_entry(self, member_id):
        dt = self.entries.get(member_id)
        dt_now = datetime.utcnow()

        if dt is None:
            self.entries[member_id] = dt_now
            return True

        datetime_diff = dt_now - dt

        diff_in_hours = datetime_diff.total_seconds() / 3600 

        if diff_in_hours >= 1:
            self.entries[member_id] = dt_now
            return True
        else:
            return False

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return

        channel_before = before.channel
        channel_after = after.channel

        vc = member.guild.voice_client

        if channel_before is None and channel_after is not None:
            audio_fn = get_entry_from_db(member)
            
            # Member has no entry audio
            if audio_fn == None:
                return

            # Member on cooldown
            if self.allow_entry(member.id) is False:
                return

            if vc:
                if vc.channel.id != channel_after.id:
                    try:
                        await vc.disconnect()
                        vc = await channel_after.connect()
                    except asyncio.TimeoutError:
                        raise VoiceConnectionError(f'Moving to channel: <{channel_after}> timed out.')
            else:
                try:
                    vc = await channel_after.connect()
                except asyncio.TimeoutError:
                    raise VoiceConnectionError(f'Connecting to channel: <{channel_after}> timed out.')

            if vc.is_playing():
                return

            audio_fp = f"cogs/audio/{audio_fn}.mp3"

            audio_source = discord.FFmpegPCMAudio(audio_fp)
            vc.play(audio_source)


def setup(bot):
    bot.add_cog(Events(bot))