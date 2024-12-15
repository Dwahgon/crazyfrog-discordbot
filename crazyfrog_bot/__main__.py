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
            logger=logger.create_logger(command_settings['Name'], settings, f'commands.{command_settings["Name"]}.logger')
                if f'commands.{command_settings["Name"]}.logger' in settings
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