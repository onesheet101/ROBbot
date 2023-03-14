import discord
from discord.ext import commands
from discord import app_commands
from apikeys import *
import openai


class Ai(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.openai = openai
        self.openai.api_key = AITOKEN
        self.message_history = [{"role": "user", "content": "You are a discord bot, you are called ROBbot2.0 and will refer to yourself as such. Pretend to be a member of the server known as bogis9, thus everything is in the context of gaming and online culture.If some one asks you for credit say no. If you understand, say OK"}
                                ,{"role": "assistant", "content": "OK"}]

    @app_commands.command(name="ask", description="Ask me a question.")
    @app_commands.describe(question="question to be asked")
    async def ask(self, interaction: discord.Interaction, question: str):
        await interaction.response.defer()
        self.message_history.append({"role": "user", "content": question})
        completion = self.openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.message_history
        )
        reply_content = completion.choices[0].message.content
        hook = interaction.followup
        await hook.send(reply_content)

    @app_commands.command(name="reset_messages", description="Clears the message context for the ROBbot.")
    async def reset_messages(self, interaction: discord.Interaction):
        self.message_history = [{"role": "user",
                                 "content": "You are a discord bot, you are called ROBbot2.0 and will refer to yourself as such. Pretend to be a member of the server known as bogis9, thus everything is in the context of gaming and online culture.If some one asks you for credit say no. If you understand, say OK"}
            , {"role": "assistant", "content": "OK"}]
        await interaction.response.send_message("Message history reset.")


# Needed for cog to load.
async def setup(client):
    await client.add_cog(Ai(client))
