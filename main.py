import discord
import os
# load our local env so we dont have the token in public
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_dl import YoutubeDL
import urllib.parse, urllib.request, re

load_dotenv()
client = commands.Bot(command_prefix='*')  # prefix our commands with '*'

players = {}


@client.event  # check if bot is ready
async def on_ready():
    print('Bot online')


# command for bot to join the channel of the user, if the bot has already joined and is in a different channel, it will move to the channel the user is in
@client.command()
async def ay(ctx):
    if ctx.author.voice is None:
      await ctx.send("Shala Age VC Te Connect Ho!")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
      await voice_channel.connect()
      await ctx.send("Ami Eshechi Tomader Gaan Shonate!")
    else:
      await ctx.voice_client.move_to(voice_channel)


# command to play sound from a youtube URL
@client.command()
async def gaanko(ctx, *, search):

    print("1")
    print(search)
    
    query_string = urllib.parse.urlencode({
      'search_query': search
      })

    print("2")
    print(query_string)

    htm_content = urllib.request.urlopen(
      'http://www.youtube.com/results?' + query_string
      )

    print("3")
    print(htm_content)

    search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())

    print("4")
    print(search_results[0])

    url = 'https://www.youtube.com/watch?v=' + search_results[0]

    print("5")
    print(url)

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        await ctx.send('Naw Shono - ' + search)
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()

# check if the bot is already playing
    else:
        await ctx.send("Abe Tham Ekta Gaan Kocchi Tw")
        return


# command to resume voice if it is paused
@client.command()
async def abarko(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        await ctx.send('Naw Shono Abar')
        voice.resume()


# command to pause voice if it is playing
@client.command()
async def dara(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        await ctx.send('Apun Pause Ho Gaya')
        voice.pause()


# command to stop voice
@client.command()
async def chup(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        await ctx.send('Khaaaaataaaaaammmmm...')
        voice.stop()

@client.command()
async def vag(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    await ctx.voice_client.disconnect()
    await ctx.send("Biday Pitibi!")

# command to clear channel messages
@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send("Messages have been cleared")


#my_secret = os.environ['TOKEN']

client.run(ODk2MDkyMzY2MzcxNDIyMjUw.YWCFDA.jRtCeDzekPXXrqHc7XVoGnXSTeo)

