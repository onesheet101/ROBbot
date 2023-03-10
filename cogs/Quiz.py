import discord
from discord.ext import commands
from discord import app_commands
import random
from datetime import timedelta
from questions import *
from Timer import Timer


class Quiz(commands.Cog):

    def __init__(self, client):
        self.client = client

    timers = {}
    answered = {}

    # Whenever a user goes from having no voice_state to having one
    # has a 1/100 chance of initiating a quiz for them.
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member == self.client.user:
            return
        if before.channel is None and after.channel:
            randomnumber = random.randint(0, 100)
            if randomnumber == 100:
                await self.begin_quiz(member)

    # Manual way of forcing a quiz question.
    # Note: Does not work in DM channel must be in guild channel.
    @app_commands.command(name="giveq", description="Gives a question")
    async def giveq(self, interaction: discord.Interaction):
        member = await interaction.guild.fetch_member(interaction.user.id)
        await self.begin_quiz(member)

    # Just sends a list of all current timer objects to user.
    @app_commands.command(name="gettimers", description="Gives list of all active question timers.")
    async def gettimers(self, interaction: discord.Interaction):
        await interaction.user.send(self.timers)

    # Displays the embedded question the user has to answer in their dm.
    # This embedded question includes three reactions to take the answer.
    # The timer for the question is also created here before calling "take_answer".
    async def begin_quiz(self, member):
        # Retrieves a random question from an array in "questions.py"
        randomnumber = random.randint(0, len(questions))
        question = questions[randomnumber][0]
        questionanswers = questions[randomnumber][1:-1]
        answer = questions[randomnumber][4]
        # ----------------------------------------------------------
        embed = discord.Embed(title="Question Time", description=question,
                              colour=0x9e4df0)
        embed.add_field(name=questionanswers[0], value="1")
        embed.add_field(name=questionanswers[1], value="2")
        embed.add_field(name=questionanswers[2], value="3")
        await member.send("You have 5 minutes to answer the question below.\n"
                          "Failure to do so or get the wrong answer you will be\n"
                          "timed out for 5 minutes. Answer by ticking the correct reaction.")
        message = await member.send(embed=embed)
        await message.add_reaction('1️⃣')
        await message.add_reaction('2️⃣')
        await message.add_reaction('3️⃣')
        await self.add_timer(member)
        await self.take_answer(message, answer, member)

    # Creates a loop that will only break if the user reacts to embedded question.
    # Currently, does not listen for specific reaction so technically doesn't have to answer question.
    async def take_answer(self, message, answer, member):
        reacted = False
        while not reacted:
            payload = await self.client.wait_for("raw_reaction_add")
            if payload.message_id == message.id:
                reacted = True
                await self.did_answer(payload, answer, member)
        return

    # Removes timer object for the associated user.
    # Updates "answered" to let end_of_timer know that the user answered.
    # Sends correct if answer is correct and gives a timeout if the user is not.
    async def did_answer(self, payload, answer, member):
        self.timers.pop(member.id)
        self.answered[member.id] = "yes"
        if payload.emoji.name == answer:
            await member.send("Correct")
        else:
            await member.timeout(timedelta(minutes=5), reason="You got it wrong boy")
            print(f'{member} got the answer incorrect and was timed out for 5 minutes.')

    # Simply instantiates the new timer object for the user and adds to dictionary.
    async def add_timer(self, member):
        new_timer = Timer(self, member)
        self.timers[member.id] = new_timer

    # Is called when the timer object finishes its timer.
    # Checks "answered" if no value is found it hands out a timeout.
    # The timer dictionary is then cleared.
    async def end_of_timer(self, member):
        if self.answered.pop(member.id, None) is None:
            await member.timeout(timedelta(minutes=5), reason="You did not answer in time.")
            print(f'{member} did not answer and was time out for 5 minutes.')
        self.timers.pop(member.id)

# Needed for cog to load.
async def setup(client):
    await client.add_cog(Quiz(client))
