import discord
import logging

class AudioPlayer:
    def __init__(self, audio_file: str, logger: logging.Logger):
        self.logger = logger
        self.audio_file = audio_file
        pass

    async def audio_player(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        channel = None
        if before.channel is not None:
            channel = before.channel
            self.logger.info(f"{member.name} left a channel")
        elif after.channel is not None:
            channel = after.channel
            self.logger.info(f"{member.name} joined a channel")

        if channel is None:
            self.logger.warning("on_voice_state_update was triggered but no channel was found")
            return

        self.logger.debug(f'Before channel: {before.channel}; After channel: {after.channel}')
        if (before.channel is None) != (after.channel is None):
            voice_client = channel.guild.voice_client
            if voice_client is not None:
                self.logger.debug("We're already in a voice channel")

                alone = len(voice_client.channel.members) == 1
                # Se um bot entrar, ou se tivermos sozinho no canal, sai
                if alone:
                    self.logger.info("Leaving channel because we're alone")
                    await voice_client.disconnect()
                return

            self.logger.debug("We're not in a voice channel")

            if len(channel.members) == 0:
                self.logger.debug("Not joining voice channel because it's empty")
                return

            self.logger.info("Joining voice channel")
            await channel.connect()

            # TODO: make this more efficient and not display an error if user leaves channel
            self.logger.info("Playing music")
            def play_audio():
                audio_source = discord.FFmpegPCMAudio(self.audio_file)
                def after_play_audio(e):
                    if e is None:
                        self.logger.info("Looping Music")
                        audio_source.cleanup()
                        play_audio()
                    else:
                        self.logger.error('Player error: %s' % e)
                channel.guild.voice_client.play(audio_source, after=after_play_audio)
            play_audio()