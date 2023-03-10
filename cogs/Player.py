import discord
from discord.ext import commands
from discord import app_commands
from discord import FFmpegPCMAudio
from discord.app_commands import Choice


class Player(commands.Cog):

    def __init__(self, client):
        self.client = client

    queues = {}

    # Makes the ROBbot join the voice channel the user is in when the command is called.
    @app_commands.command(name="join", description="Makes the ROBbot join the VC you are in.")
    async def join(self, interaction: discord.Interaction):
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            voice = await channel.connect()
        else:
            await interaction.response.send_message("You must be a voice channel to do this command.")

    # Forces the ROBbot to leave the voice channel it is currently in.
    @app_commands.command(name="leave", description="Makes the ROBbot leave any VC.")
    async def leave(self, interaction: discord.Interaction):
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect()
        else:
            await interaction.response.send_message("I must be in a voice channel for this command to work.")

    # Makes the ROBbot pause any audio it is currently playing.
    @app_commands.command(name="pause", description="Pauses what the ROBbot is playing")
    async def pause(self, interaction: discord.Interaction):
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)  # Retrieves the bot voice client.
        if voice.is_playing():
            voice.pause()
        else:
            await interaction.response.send_message("Nothing is playing, to pause.")

    # The ROBbot will continue playing any audio it had paused.
    @app_commands.command(name="resume", description="ROBot will carry on playing what was paused.")
    async def resume(self, interaction: discord.Interaction):
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await interaction.response.send("Nothing is paused.")

    # Will stop the audio and remove it entirely from playing.
    @app_commands.command(name="stop", description="ROBot will clear the song it is currently playing.")
    async def stop(self, interaction: discord.Interaction):
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        if voice.is_playing() or voice.is_paused():
            voice.stop()
        else:
            await interaction.response.send_message("Nothing is playing")

    # Gives the user three options to play, for the /play command.
    @app_commands.command(name="play", description="ROBbot will play a song.")
    @app_commands.describe(arg="Song to Play")
    @app_commands.choices(arg=[
        Choice(name="Cheef Keef", value="keef"),
        Choice(name="Couple Guinness", value="song"),
        Choice(name="Kid", value="kid"),
    ])
    async def play(self, interaction: discord.Interaction, arg: Choice[str]):
        voice = interaction.guild.voice_client
        # Gets the appropriate source for song selected.
        song = arg.value + '.mp3'
        source = FFmpegPCMAudio("./Audio/" + song)
        # Plays the source to the voice-client, calls self.check_queue once source is finished.
        player = voice.play(source, after=lambda x=None: self.check_queue(interaction, interaction.guild.id))
        embed = discord.Embed(title="Now Playing", description=arg.name, colour=0x9e4df0)
        await interaction.response.send_message(embed=embed)

    # Allows user to queue an audio clip, currently has to type no options have been added.
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

    # Called every time audio finishes playing, checks if another source is in the queue to be played and plays it.
    def check_queue(self, ctx, id):
        if self.queues[id]:
            voice = ctx.guild.voice_client
            source = self.queues[id].pop(0)
            player = voice.play(source, after=lambda x=None: self.check_queue(ctx, ctx.guild.id))

# Needed for loading cog.
async def setup(client):
    await client.add_cog(Player(client))
