import discord
import logging
from typing import Callable

class DiscordClient(discord.Client):
    def __init__(self, *, intents, logger: logging.Logger, **options):
        super().__init__(intents=intents, **options)
        self.logger = logger
        self.tree: discord.app_commands.CommandTree = None
        self._voice_state_update_listeners: list[Callable[[discord.Member, discord.VoiceState, discord.VoiceState], None]] = []

    async def on_ready(self):
        if self.tree is not None:
            self.logger.info("Starting command tree...")
            await self.tree.sync()
        else:
            await self.logger.warning("Started without settings command tree")
            return
        self.logger.info("Discord bot started")

    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        for listener in self._voice_state_update_listeners:
            await listener(member, before, after)

    def add_voice_state_update_listener(self, listener: Callable[[discord.Member, discord.VoiceState, discord.VoiceState], None]):
        self._voice_state_update_listeners.append(listener)
