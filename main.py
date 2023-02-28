#Dependencies
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import requests
import json

#Api Tokens
from apikeys import *
intents = discord.Intents.all()

queues = {}
def check_queue(ctx,id):
    if queues[id] != []:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        player = voice.play(source,after=lambda x=None: check_queue(ctx,ctx.guild.id))

client = commands.Bot(command_prefix='//', intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="pyCharm"))
    print("Bot Is Running!")
    print("---------------")

@client.command()
async def hello(ctx):
    await ctx.send("Working")

@client.command()
async def covid(ctx):
    url = "https://vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com/api/npm-covid-data/world"

    headers = {
        "X-RapidAPI-Key": COVIDTOKEN,
        "X-RapidAPI-Host": "vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)
    CovidArray = json.loads(response.text)
    newdeaths = CovidArray[0]['NewDeaths']
    await ctx.send(f'Global new deaths are {newdeaths}')

@client.command()
async def join(ctx):
    if(ctx.author.voice):
        channel = ctx.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('song.mp3')
        player = voice.play(source)
    else:
        await ctx.send("You must be a voice channel to do this command.")

@client.command()
async def leave(ctx):
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("I must be in a voice channel for this command to work.")

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Nothing is playing, to pause.")

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("Nothing is paused.")

@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing() or voice.is_paused():
        voice.stop()
    else:
        await ctx.send("Nothing is playing")

@client.command()
async def play(ctx, arg):
    voice = ctx.guild.voice_client
    song = arg + '.mp3'
    source = FFmpegPCMAudio(song)
    player = voice.play(source, after=lambda x=None: check_queue(ctx,ctx.guild.id))
    embed = discord.Embed(title="Now Playing", description=arg, colour = 0x9e4df0)
    await ctx.send(embed=embed)


@client.command()
async def queue(ctx, arg):
    voice = ctx.guild.voice_client
    song = arg + '.mp3'
    source = FFmpegPCMAudio(song)

    guild_id = ctx.guild.id

    if guild_id in queues:
        queues[guild_id].append(source)
    else:
        queues[guild_id] = [source]

    await ctx.send("Added to queue")

@client.event
async def on_message(message):
    count = message.content.count("rocket")
    if count != 0:
        await message.delete()
        await message.channel.send("NO ROCKET LEAGUE ALLOWED")
    else:
        await client.process_commands(message)

@client.command()
async def embed(ctx):
    embed = discord.Embed(title="test",url="https://github.com/onesheet101/ROBbot",description="my github pog",colour=0x9e4df0)
    embed.set_author(name="Robert S", url="https://github.com/onesheet101",icon_url="https://avatars.githubusercontent.com/u/126177072?v=4")
    embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/126177072?v=4")
    await ctx.send(embed=embed)













client.run(BOTTOKEN)