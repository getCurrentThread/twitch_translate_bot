import os
import sys
import urllib.request
from functools import wraps

from pathlib import Path
import json

import twitchio
import cogs
from twitchio.ext import commands


class Bot(commands.Bot):

    def __init__(self, settings):
        super().__init__(irc_token=settings['bot_irc_token'],
                         client_id= settings['bot_client_id'],
                         nick=settings['bot_nick'], prefix='!',
                         initial_channels=settings['bot_initial_channels'])
        for key in ['bot_irc_token', 'bot_client_id', 'bot_nick', 'bot_initial_channels']:
            del settings[key]
        self.settings = settings

    async def load_all_extensions(self):
        print('Attempting to load modules...')
        cog_dir = Path.cwd() / 'modules'
        cogs = [x.stem for x in Path(cog_dir).glob('*.py')]
        for cog in cogs:
            try:
                self.load_module(f'modules.{cog}')
                print(f'{cog}: SUCCESS')
            except Exception as e:
                error = f'{cog}: FAIL -- {type(e).__name__} : {e}'
                print(f'{error}')

    async def event_ready(self):
        await self.load_all_extensions()
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        await self.handle_commands(message)

if __name__ == '__main__':
    with open("settings.json", "r") as f:
        settings = json.load(f)

    bot = Bot(settings)
    bot.run()
