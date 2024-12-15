import discord
import logging
import random

def setup(tree: discord.app_commands.CommandTree, name: str, description: str, logger: logging.Logger, extra_args = {}):
    @tree.command(name=name, description=description)
    async def command(interation: discord.Interaction):
        logger.info(f'User ({interation.user.id}) {interation.user.name} used /{name}')
        images = extra_args['images']
        texts = extra_args['texts']

        image = images[random.randint(0, len(images))]
        text = texts[random.randint(0, len(images))]
        logger.debug(f'Chosen image: {image}')
        logger.debug(f'Chosen text: {text}')

        embed = discord.Embed()
        embed.set_image(url=image)
        await interation.response.send_message(text, embed=embed)