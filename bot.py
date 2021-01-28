import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
from os import system
from discord import Spotify
import spotdl

client = commands.Bot(command_prefix = ".")
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('With my own life'))
    print('Bot is ready.')
    print("Logged in as: " + client.user.name + "\n")

@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"the bot is connected to {channel}\n")

    await ctx.send(f"joined{channel}")

@client.command(pass_context=True)
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    
    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"the bot has left{channel}")
        await ctx.send(f"left{channel}")
    else:
        print("not in one")
        await ctx.send("not in one")

@client.command(pass_context=True)
async def download(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file,but it is being played")
        await ctx.send("Error: Music playing")
        return
    
    await ctx.send("Getting everything ready now")

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format':'bestaudio/best',
        'postprocessors':[{
            'key':'FFmpegExtractAudio',
            'preferredcodec':'mp3',
            'preferredquality':'192',
        }],
    }
    try:    
       with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])
            await ctx.send("Downloaded the song")
            await ctx.send("https://github.com/ishanrajpal/git.py/blob/master/song.mp3")
    except Exception as o:
        print("Fallback: youtube-dl does not support this url ,using spotify")
        #c_path = os.path.dirname(os.path.realpath(__file__))
        system("spotdl -f " + '"' + "./" + '"' + " -s " + url +" -i " +"automatic")
        await ctx.send("Downloaded the song")
        await ctx.send("https://github.com/ishanrajpal/git.py/blob/master/song.mp3")


client.run(os.environ['Discord_token'])

