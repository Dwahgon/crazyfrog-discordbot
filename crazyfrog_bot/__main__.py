# import os
# import discord
# import random
# import 

# from dotenv import load_dotenv
# from discord.ext import commands
# from settings import CRAZYFROG_URL, CRAZYFROG_MUSICAS, CRAZYFROG_IMAGES, CRAZYFROG_FRASES, CRAZYFROG_PREFIX

# load_dotenv()
# intents = discord.Intents(
#     guilds=True, voice_states=True, members=True, messages=True)
# bot = commands.Bot(command_prefix=commands.when_mentioned_or(CRAZYFROG_PREFIX),
#                    description='Relatively simple music bot example',
#                    intents=intents)


# async def play(ctx, channel: discord.VoiceChannel):
#     """Toca uma musica aleatoria do crazy frog"""
#     if ctx.guild.voice_client is None:
#         await channel.connect()
#     else:
#         await ctx.voice_client.move_to(channel)

#     reproduzir_video(channel, pegar_el_aleatorio(CRAZYFROG_MUSICAS))


# @bot.event
# async def on_ready():
#     print('Logged in as {0} ({0.id})'.format(bot.user))
#     print('------')

#     for guild in bot.guilds:
#         for voice_channel in guild.voice_channels:
#             members = voice_channel.members
#             if len(members) > 0:
#                 has_bot = False
#                 for member in members:
#                     if member.bot:
#                         has_bot = True
#                         break

#                 if has_bot:
#                     continue

#                 await voice_channel.connect()
#                 await reproduzir_video(voice_channel, CRAZYFROG_URL)
#                 print("Tocando crazy frog")
#                 break


# @bot.event
# async def on_voice_state_update(member, before, after):
#     # Canal
#     channel = None
#     if before.channel is not None:
#         channel = before.channel
#         print(member.name+" saiu de um canal")
#     elif after.channel is not None:
#         channel = after.channel
#         print(member.name+" entrou em um canal")

#     if channel is None:
#         print("Deu pau")
#         return

#     voice_client = channel.guild.voice_client

#     # Alguem entrou ou saiu de um canal
#     if not before.channel and after.channel or before.channel and not after.channel:
#         # Ja estamos tocando crazy frog
#         if voice_client is not None:
#             print("Ja estamos tocando crazy frog")

#             bot_entrou = before.channel is None and after.channel is not None and after.channel == voice_client.channel and member != bot.user and member.bot
#             estamos_sozinho = len(voice_client.channel.members) == 1
#             # Se um bot entrar, ou se tivermos sozinho no canal, sai
#             if bot_entrou or estamos_sozinho:
#                 print("Saindo: Estamos sozinho: "+str(estamos_sozinho) +
#                       "; Bot entrou: "+str(bot_entrou))
#                 await voice_client.disconnect()
#             return

#         print("Nao estamos tocando crazy frog")

#         # Checar se o canal ja tem bot
#         for m in channel.members:
#             if m.bot:
#                 print("O canal que esse usuario entrou ja tem bot, faz nada")
#                 return

#         # Checar se o canal tem gente
#         if len(channel.members) == 0:
#             return

#         await channel.connect()
#         await reproduzir_video(channel, CRAZYFROG_URL)
#         print("Tocando crazy frog")


# async def reproduzir_video(canal, url):
#     player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
#     canal.guild.voice_client.play(player, after=lambda e: print(
#         'Player error: %s' % e) if e else None)

import discord
import dotenv
import configparser
import commands as commands
from audio_player import AudioPlayer
import logger
import discord_client as discord_client
import re
import os
import ast

def main():
    dotenv.load_dotenv()

    settings = configparser.ConfigParser()
    settings.read("settings.conf")

    main_logger = logger.create_logger('main', settings, 'main.logger')
    client_logger = logger.create_logger('Discord Bot', settings, 'client.logger')

    main_logger.debug("Creating discord objects")
    intents = discord.Intents(guilds=True, voice_states=True, members=True, messages=True)
    client = discord_client.DiscordClient(intents=intents, logger=client_logger)
    tree = discord.app_commands.CommandTree(client)
    client.tree = tree
    audio_player = AudioPlayer(settings['client.audio_player']["AudioFile"], logger=logger.create_logger("Audio player", settings, f'client.audio_player.logger')
                if f'commands.audio_player.logger' in settings
                else client_logger,)
    client.add_voice_state_update_listener(lambda member, before, after: audio_player.audio_player(member, before, after))

    main_logger.debug("Loading commands")
    for command_settings in [settings[k] for k in settings.keys() if re.match(r'^commands\.\w*', k)]:
        main_logger.info(f"Using '{command_settings['Name']}' command")
        commands.ALL_COMMANDS[command_settings['Type']](
            tree=tree,
            name=command_settings['Name'],
            description=command_settings['Description'],
            logger=logger.create_logger(command_settings['Name'], settings, f'commands.{command_settings['Name']}.logger')
                if f'commands.{command_settings['Name']}.logger' in settings
                else client_logger,
            extra_args={
                'response': command_settings['Response'] if 'Response' in command_settings else '',
                'images': ast.literal_eval(command_settings['Images']) if 'Images' in command_settings else '',
                'texts': ast.literal_eval(command_settings['Texts']) if 'Texts' in command_settings else '',
            }
        )

    main_logger.debug("Running client")
    client.run(os.getenv("CRAZYFROG_DISCORD_BOT_TOKEN"))

if __name__ == '__main__':
    main()