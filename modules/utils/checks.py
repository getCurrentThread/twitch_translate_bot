import os

"""
@author: bsquidwrd
@source: https://github.com/bsquidwrd/Example-TwitchIO-Bot/blob/master/cogs/utils/checks.py
"""

#def is_owner(ctx):
#    return ctx.message.author.id == int(os.environ['OWNER_ID'])

def is_mod(ctx):
    return ctx.message.author.is_mod == 1