import discord
from discord.ext import commands
from discord import app_commands
import random
from datetime import timedelta
from questions import *


class Quiz(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member == self.client.user or after.channel is None:
            return
        randomnumber = random.randint(0, 100)
        if randomnumber == 100:
            await self.begin_quiz(member)

    @app_commands.command(name="giveq", description="Gives a question")
    async def giveq(self, interaction: discord.Interaction):
        await self.begin_quiz(interaction.user)

    # Is called 1/100 a voice-state is updated excluding leaving channels.
    # Displays the embedded question the user has to asnwer in their dm.
    async def begin_quiz(self, member):
        randomnumber = random.randint(0, 2)
        question = questions[randomnumber][0]
        questionanswers = questions[randomnumber][1:-1]
        answer = questions[randomnumber][4]
        embed = discord.Embed(title="Question Time", description=question,
                              colour=0x9e4df0)
        embed.add_field(name=questionanswers[0], value="1")
        embed.add_field(name=questionanswers[1], value="2")
        embed.add_field(name=questionanswers[2], value="3")
        message = await member.send(embed=embed)
        await message.add_reaction('1️⃣')
        await message.add_reaction('2️⃣')
        await message.add_reaction('3️⃣')
        await self.take_answer(message, answer, member)

    async def take_answer(self, message, answer, member):
        reacted = False
        while not reacted:
            payload = await self.client.wait_for("raw_reaction_add")
            if payload.message_id == message.id:
                reacted = True
                await self.did_answer(payload, answer, member)
        return

    async def did_answer(self, payload, answer, member):
        if payload.emoji.name == answer:
            await member.send("Correct")
        else:
            await member.timeout(timedelta(minutes=5), reason="You got it wrong boy")

    async def did_not_answer(self):
        pass


async def setup(client):
    await client.add_cog(Quiz(client))
