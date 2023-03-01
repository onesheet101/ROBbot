from discord.ext import commands
from discord import app_commands
import requests
import json
import discord
from apikeys import *


class Greetings(commands.Cog):

    def __init__(self, client):
        self.client = client

    @app_commands.command(name="hello", description="Testing")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Working")

    @app_commands.command(name="covid", description="See how many recently died due to covid globally.")
    async def covid(self, interaction: discord.Interaction):
        url = "https://vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com/api/npm-covid-data/world"

        headers = {
            "X-RapidAPI-Key": COVIDTOKEN,
            "X-RapidAPI-Host": "vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers)
        CovidArray = json.loads(response.text)
        newdeaths = CovidArray[0]['NewDeaths']
        await interaction.response.send_message(f'Global new deaths are {newdeaths}')

    @app_commands.command(name="embed", description="Sends a test embedded messaged")
    async def embed(self, interaction: discord.Interaction):
        embed = discord.Embed(title="test", url="https://github.com/onesheet101/ROBbot", description="my github pog",
                              colour=0x9e4df0)
        embed.set_author(name="Robert S", url="https://github.com/onesheet101",
                         icon_url="https://avatars.githubusercontent.com/u/126177072?v=4")
        embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/126177072?v=4")
        await interaction.response.send_message(embed=embed)


async def setup(client):
    await client.add_cog(Greetings(client))

