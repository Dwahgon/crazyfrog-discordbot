import discord
import logging
import random
import re
from utils.regex import URL_REGEX


def setup(tree: discord.app_commands.CommandTree, name: str, description: str, logger: logging.Logger, extra_args = {}):
    tabu_images = []
    tabu_texts = []
    @tree.command(name=name, description=description)
    async def command(interation: discord.Interaction):
        logger.info(f'User ({interation.user.id}) {interation.user.name} used /{name}')
        images = extra_args['images']
        texts = extra_args['texts']

        img_index = random.randint(0, len(images))
        while img_index in tabu_images:
            img_index = random.randint(0, len(images))

        text_index = random.randint(0, len(texts))
        while text_index in tabu_texts:
            text_index = random.randint(0, len(texts))

        tabu_images.append(img_index)
        if len(tabu_images) > extra_args['image tabu size']:
            tabu_images.pop(0)

        tabu_texts.append(text_index)
        if len(tabu_texts) > extra_args['text tabu size']:
            tabu_texts.pop(0)

        image = images[img_index]
        text = texts[text_index]
        logger.debug(f'Chosen image: {image}')
        logger.debug(f'Chosen text: {text}')

        if re.match(URL_REGEX, image):
            embed = discord.Embed()
            embed.set_image(url=image)
            await interation.response.send_message(text, embed=embed)
        else:
            await interation.response.send_message(text, file=discord.File(image))