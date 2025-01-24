import discord
import logging
import random
import re
from utils.regex import URL_REGEX


def setup(tree: discord.app_commands.CommandTree, name: str, description: str, logger: logging.Logger, extra_args = {}):
    @tree.command(name=name, description=description)
    async def command(interation: discord.Interaction):
        logger.info(f'User ({interation.user.id}) {interation.user.name} used /{name}')
        images = extra_args['images']
        texts = extra_args['texts']

        image = images[random.randint(0, len(images))]
        text = texts[random.randint(0, len(texts))]
        logger.debug(f'Chosen image: {image}')
        logger.debug(f'Chosen text: {text}')

        if re.match(URL_REGEX, image):
            embed = discord.Embed()
            embed.set_image(url=image)
            await interation.response.send_message(text, embed=embed)
        else:
            await interation.response.send_message(text, file=discord.File(image))