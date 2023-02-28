import discord
from discord.ext import commands
from discord import FFmpegPCMAudio

class Music(commands.Cog):

    def __init__(self,client):
        self.client = client

    queues = {}

    @commands.command()
    async def join(self, ctx):
        if (ctx.author.voice):
            channel = ctx.author.voice.channel
            voice = await channel.connect()
        else:
            await ctx.send("You must be a voice channel to do this command.")

    @commands.command()
    async def leave(self, ctx):
        if (ctx.voice_client):
            await ctx.guild.voice_client.disconnect()
        else:
            await ctx.send("I must be in a voice channel for this command to work.")

    @commands.command()
    async def pause(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("Nothing is playing, to pause.")

    @commands.command()
    async def resume(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("Nothing is paused.")

    @commands.command()
    async def stop(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing() or voice.is_paused():
            voice.stop()
        else:
            await ctx.send("Nothing is playing")

    @commands.command()
    async def play(self, ctx, arg):
        voice = ctx.guild.voice_client
        song = arg + '.mp3'
        source = FFmpegPCMAudio(song)
        player = voice.play(source, after=lambda x=None: self.check_queue(ctx, ctx.guild.id))
        embed = discord.Embed(title="Now Playing", description=arg, colour=0x9e4df0)
        await ctx.send(embed=embed)

    @commands.command()
    async def queue(self, ctx, arg):
        voice = ctx.guild.voice_client
        song = arg + '.mp3'
        source = FFmpegPCMAudio(song)

        guild_id = ctx.guild.id

        if guild_id in self.queues:
            self.queues[guild_id].append(source)
        else:
            self.queues[guild_id] = [source]

        await ctx.send("Added to queue")

    def check_queue(self, ctx, id):
        if self.queues[id]:
            voice = ctx.guild.voice_client
            source = self.queues[id].pop(0)
            player = voice.play(source, after=lambda x=None: self.check_queue(ctx, ctx.guild.id))

async def setup(client):
    await client.add_cog(Music(client))

