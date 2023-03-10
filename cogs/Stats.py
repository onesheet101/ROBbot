from apikeys import *
from discord.ext import commands
from discord import app_commands
import mysql.connector
import mysql
import discord


class Stats(commands.Cog):
    db = mysql.connector.connect(host=dhost, user=duser, passwd=dpasswd, database="discord")
    mycursor = db.cursor()

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        membername = str(member)
        mid = member.id
        try:
            self.mycursor.execute("INSERT INTO member (name, score, memberID) VALUES (%s,%s,%s)", (membername, 1000, mid))
            self.db.commit()
        except:
            print(f'{membername} already has a record.')

    @app_commands.command(name="my_credit", description="Gives your credit score")
    async def my_credit(self, interaction: discord.Interaction):
        currentscore = self.get_score(interaction.user.id)
        await interaction.response.send_message(f'Your credit is currently {currentscore}')

    @app_commands.checks.has_role(311225669289902090)
    @app_commands.command(name="add_credit", description="Add credit to a given memberID.")
    @app_commands.describe(member="member to give credit to", amount="amount to add")
    async def add_credit(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        newscore = self.add_score(member.id, amount)
        await interaction.response.send_message(f'The score of {member} is now: {newscore}')

    @app_commands.checks.has_role(311225669289902090)
    @app_commands.command(name="reduce_credit", description="Reduce credit from a given memberID.")
    @app_commands.describe(member="member to reduce credit from")
    async def reduce_credit(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        newscore = self.remove_score(member.id, amount)
        await interaction.response.send_message(f'The score of {member} is now: {newscore}')

    @app_commands.command(name="check_credit", description="Check the credit of a given memberID.")
    @app_commands.describe(member="member to check credit")
    async def check_credit(self, interaction: discord.Interaction, member: discord.Member):
        currentscore = self.get_score(member.id)
        await interaction.response.send_message(f'The score of {member} is {currentscore}')

    @app_commands.checks.has_role(311225669289902090)
    @app_commands.command(name="reset_credit", description="Reset the credit of a given memberID.")
    @app_commands.describe(member="member to reset credit")
    async def reset_credit(self, interaction: discord.Interaction, member: discord.Member):
        self.reset_score(member.id)
        await interaction.response.send_message(f'The score of {member} is now: 1000')

    def get_score(self, memberid):
        unpacked = []
        self.mycursor.execute("SELECT score FROM member WHERE memberID = %s", (memberid,))
        for record in self.mycursor:
            return record[0]

    def add_score(self, memberid, amount):
        currentscore = self.get_score(memberid)
        amount += currentscore
        self.mycursor.execute("UPDATE member SET score = %s WHERE memberID = %s", (amount, memberid))
        self.db.commit()
        return amount

    def remove_score(self, memberid, amount):
        currentscore = self.get_score(memberid)
        amount = currentscore - amount
        self.mycursor.execute("UPDATE member SET score = %s WHERE memberID = %s", (amount, memberid))
        self.db.commit()
        return amount

    def reset_score(self,memberid):
        self.mycursor.execute("UPDATE member SET score = %s WHERE memberID = %s", (1000, memberid))
        self.db.commit()


async def setup(client):
    await client.add_cog(Stats(client))
