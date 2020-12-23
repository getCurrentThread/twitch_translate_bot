import logging
import os
from pathlib import Path

from twitchio.ext import commands

from modules.utils import checks

'''
@author : robertwayne
@source : https://github.com/robertwayne/nullbot

'''


class ManageCog(commands.AutoCog):

    def __init__(self, bot):
        self.bot = bot

    def _prepare(self, bot):
        pass

    @commands.command()
    #@commands.check(checks.is_mod)
    async def load(self, ctx, *, cog):
        try:
            root = Path(__file__).parents[1]
            cog_path = (root / f'modules/{cog}.py')
            if os.path.exists(cog_path):
                self.bot.load_module(f'modules.{cog}')
                await ctx.send('Loaded ' + str(cog) + ' successfully.')
            else:
                await ctx.send('Cannot find ' + str(cog) + '.')
        except Exception as e:
            error = f'Unable to load {cog}.\n'
            logging.exception(e)
            await ctx.send(error)

    @commands.command()
    #@commands.check(checks.is_mod)
    async def unload(self, ctx, *, cog):
        try:
            root = Path(__file__).parents[1]
            cog_path = (root / f'modules/{cog}.py')
            if os.path.exists(cog_path):
                self.bot.unload_module(f'modules.{cog}')
                await ctx.send('Unloaded ' + str(cog) + ' successfully.')
            else:
                await ctx.send('Cannot find ' + str(cog) + '.')
        except Exception as e:
            error = f'Unable to unload {cog}.\n'
            logging.exception(e)
            await ctx.send(error)

    @commands.command()
    #@commands.check(checks.is_mod)
    async def reload(self, ctx, *, cog):
        try:
            root = Path(__file__).parents[1]
            cog_path = (root / f'modules/{cog}.py')
            if os.path.exists(cog_path):
                self.bot.unload_module(f'modules.{cog}')
                self.bot.load_module(f'modules.{cog}')
                await ctx.send('Reloaded ' + str(cog) + ' successfully.')
            else:
                await ctx.send('Cannot find ' + str(cog) + '.')
        except Exception as e:
            error = f'Unable to reload {cog}.\n'
            logging.exception(e)
            await ctx.send(error)

    #ping-pong
    @commands.command(name="이리와")
    async def test(self, ctx):
        await ctx.send("이거놔라 닝겐!")

def prepare(bot):
    bot.add_cog(ManageCog(bot))


def breakdown(bot):
    bot.remove_cog(ManageCog(bot))
