# Dependencies
import discord
from discord.ext import commands
import os
from apikeys import *

# Declaring discord intents for the API.
intents = discord.Intents.all()
client = commands.Bot(command_prefix='//', intents=intents)


# Is called when Bot is connected to Discord.
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="pyCharm"))
    print("Bot Is Running!")
    print("---------------")

    initial_extensions = []
    # Adds all cogs to an array.
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            initial_extensions.append("cogs." + filename[:-3])

    # Loads all cogs
    if __name__ == '__main__':
        for extension in initial_extensions:
            await client.load_extension(extension)
        print(f'{initial_extensions} are loaded')


# Command to manually sync app_commands with the discord API.
@client.command()
async def sync(ctx):
    synced = await ctx.bot.tree.sync()
    print(f'synced {len(synced)} commands')
    print(synced)


# Connects to the discord API.
client.run(BOTTOKEN)
