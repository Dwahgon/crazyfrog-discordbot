import discord
import logging

def setup(tree: discord.app_commands.CommandTree, name: str, description: str, logger: logging.Logger, extra_args = {}):
    @tree.command(name=name, description=description)
    async def command(interation: discord.Interaction):
        logger.info(f'User ({interation.user.id}) {interation.user.name} used /{name}')
        response = extra_args['response']
        await interation.response.send_message(response)