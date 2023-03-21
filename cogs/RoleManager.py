from apikeys import *
from discord.ext import commands
from discord import app_commands
import mysql.connector
import mysql
import discord
import datetime

class RoleManager(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = await self.client.fetch_guild(264905192510586882)
        role = guild.get_role(1085612173855825961)
        await member.add_roles(role, reason="New Member", atomic=True)

async def setup(client):
    await client.add_cog(RoleManager(client))