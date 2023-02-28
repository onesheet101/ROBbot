from discord.ext import commands
import requests
import json
import discord
from apikeys import *

class Greetings(commands.Cog):

    def __init__(self, client):
        self.client = client

    #command
    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Working")

    @commands.command()
    async def covid(self, ctx):
        url = "https://vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com/api/npm-covid-data/world"

        headers = {
            "X-RapidAPI-Key": COVIDTOKEN,
            "X-RapidAPI-Host": "vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers)
        CovidArray = json.loads(response.text)
        newdeaths = CovidArray[0]['NewDeaths']
        await ctx.send(f'Global new deaths are {newdeaths}')

    @commands.command()
    async def embed(self, ctx):
        embed = discord.Embed(title="test", url="https://github.com/onesheet101/ROBbot", description="my github pog",
                              colour=0x9e4df0)
        embed.set_author(name="Robert S", url="https://github.com/onesheet101",
                         icon_url="https://avatars.githubusercontent.com/u/126177072?v=4")
        embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/126177072?v=4")
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Greetings(client))