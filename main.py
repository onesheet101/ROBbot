#Dependencies
import discord
from discord.ext import commands
import requests
import json

#Api Tokens
from apikeys import *
intents = discord.Intents.all()
client = commands.Bot(command_prefix='/', intents=intents)

@client.event
async def on_ready():
    print("Bot Is Running!")
    print("---------------")

@client.command()
async def hello(ctx):
    await ctx.send("Working")

@client.command()
async def covid(ctx):
    url = "https://vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com/api/npm-covid-data/europe"

    headers = {
        "X-RapidAPI-Key": COVIDTOKEN,
        "X-RapidAPI-Host": "vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)
    CovidArray = json.loads(response.text)
    totalcases = CovidArray[2]['TotalCases']
    totaldeaths = CovidArray[2]['TotalDeaths']
    await ctx.send(f'In the UK there are a total of {totalcases} covid cases and {totaldeaths} covid deaths')






client.run(BOTTOKEN)