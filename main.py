import discord
from discord.ext import commands
from discord import app_commands
import os
from apikeys import *
from discord import Interaction
import asyncio

intents = discord.Intents.all()
client = commands.Bot(command_prefix='//', intents=intents)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="pyCharm"))
    print("Bot Is Running!")
    print("---------------")

    initial_extensions = []

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            initial_extensions.append("cogs." + filename[:-3])

    if __name__ == '__main__':
        for extension in initial_extensions:
            await client.load_extension(extension)
        print(f'{initial_extensions} are loaded')

@client.command()
async def sync(ctx):
    synced = await ctx.bot.tree.sync()
    print(f'synced {len(synced)} commands')
    print(synced)





client.run(BOTTOKEN)
