import discord
from discord.ext import commands
from discord import app_commands
from discord import FFmpegPCMAudio
from discord.app_commands import Choice


class Music(commands.Cog):

    def __init__(self, client):
        self.client = client

    queues = {}

    @app_commands.command(name="join", description="Makes the ROBbot join the VC you are in.")
    async def join(self, interaction: discord.Interaction):
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            voice = await channel.connect()
        else:
            await interaction.response.send_message("You must be a voice channel to do this command.")

    @app_commands.command(name="leave", description="Makes the ROBbot leave any VC.")
    async def leave(self, interaction: discord.Interaction):
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect()
        else:
            await interaction.response.send_message("I must be in a voice channel for this command to work.")

    @app_commands.command(name="pause", description="Pauses what the ROBbot is playing")
    async def pause(self, interaction: discord.Interaction):
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await interaction.response.send_message("Nothing is playing, to pause.")

    @app_commands.command(name="resume", description="ROBot will carry on playing what was paused.")
    async def resume(self, interaction: discord.Interaction):
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await interaction.response.send("Nothing is paused.")

    @app_commands.command(name="stop", description="ROBot will clear the song it is currently playing.")
    async def stop(self, interaction: discord.Interaction):
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        if voice.is_playing() or voice.is_paused():
            voice.stop()
        else:
            await interaction.response.send_message("Nothing is playing")

    @app_commands.command(name="play", description="ROBbot will play a song.")
    @app_commands.describe(arg="Song to Play")
    @app_commands.choices(arg = [
        Choice(name="Cheef Keef", value="keef"),
        Choice(name="Couple Guinness", value="song"),
        Choice(name="Kid", value="kid"),
    ])
    async def play(self, interaction: discord.Interaction, arg: Choice[str]):
        voice = interaction.guild.voice_client
        song = arg.value + '.mp3'
        source = FFmpegPCMAudio("./Audio/" + song)
        player = voice.play(source, after=lambda x=None: self.check_queue(interaction, interaction.guild.id))
        embed = discord.Embed(title="Now Playing", description=arg.name, colour=0x9e4df0)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="queue", description="ROBbot will queue a song.")
    @app_commands.describe(arg="Song to Play")
    async def queue(self, interaction: discord.Interaction, arg: str):
        voice = interaction.guild.voice_client
        song = arg + '.mp3'
        source = FFmpegPCMAudio("./Audio/" + song)

        guild_id = interaction.guild.id

        if guild_id in self.queues:
            self.queues[guild_id].append(source)
        else:
            self.queues[guild_id] = [source]

        await interaction.response.send_message("Added to queue")

    def check_queue(self, ctx, id):
        if self.queues[id]:
            voice = ctx.guild.voice_client
            source = self.queues[id].pop(0)
            player = voice.play(source, after=lambda x=None: self.check_queue(ctx, ctx.guild.id))


async def setup(client):
    await client.add_cog(Music(client))
