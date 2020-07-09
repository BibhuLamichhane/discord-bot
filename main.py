import os
import shutil
from os import system
import ytsearch
import discord
import youtube_dl
from discord.ext import commands
from discord.utils import get

BOT_PREFIX = ','

client = commands.Bot(command_prefix=BOT_PREFIX)

queues = {}

@client.event
async def on_ready():
    print("Bot is ready")


@client.command(pass_context=True, aliases=['j'])
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The client has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")


@client.command(pass_context=True, aliases=['l'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The client has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("client was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel")


def next_song(ctx):
    global queues
    files = os.listdir()
    voice = get(client.voice_clients, guild=ctx.guild)
    if 'Queue' in files:
        queue_files = os.listdir('./Queue')
        try:
            voice.stop()
            if 'song.mp3' in files:
                os.remove('song.mp3')   
            elif 'queue.mp3' in files:
                os.remove('queue.mp3')
            if len(queue_files):
                title = ''
                for file in queue_files:
                    title = file
                    break
                shutil.move(f'./Queue/{title}', '../')
                os.rename(f'{title}', 'queue.mp3')
                play(ctx)
        except:
            print('error')


@client.command(pass_context = True, aliases = ['p'])
async def play(ctx, url = '     '):
    global queues
    files = os.listdir()
    if url == '     ':
        pass
    else:
        try:
            if 'song.mp3' in files:
                os.remove('song.mp3')
        except PermissionError:
            pass

        if 'Queue' in files:
            shutil.rmtree('./Queue')

        await ctx.send('Downloading the audio')

        ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
        }

        try:
            if 'http' in url:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    print("Downloading audio now\n")
                    ydl.download([url])
            else:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    print("Downloading audio now\n")
                    print(url)
                    print([ytsearch.main(url)])
                    ydl.download([ytsearch.main(url)])
        except:
            ctx.send('Invalid url/video title')
        
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                print(f"Renamed File: {file}\n")
                os.rename(file, "song.mp3")
    
    files = os.listdir()
    if 'song.mp3' in files:
        voice = get(client.voice_clients, guild=ctx.guild)

        voice.play(discord.FFmpegPCMAudio('song.mp3'), after = next_song(ctx))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07
        nname = name.rsplit("-", 2)
        await ctx.send(f"Playing: {nname[1]}")

    elif 'queue.mp3' in files:
        voice = get(client.voice_clients, guild=ctx.guild)

        voice.play(discord.FFmpegPCMAudio('queue.mp3'), after = next_song(ctx))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07
        for i in queues:
            await ctx.send(f"Playing: {queues[i]}")
            queues.pop(i)
            break

    if len(queues):
        next_song(ctx)


@client.command(pass_context=True, aliases=['pa'])
async def pause(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music paused")
        voice.pause()
        await ctx.send("Music paused")
    else:
        print("Music not playing failed pause")
        await ctx.send("Music not playing failed pause")


@client.command(pass_context=True, aliases=['r', 'res'])
async def resume(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        await ctx.send("Resumed music")
    else:
        print("Music is not paused")
        await ctx.send("Music is not paused")


@client.command(pass_context=True, aliases=['s'])
async def stop(ctx):
    global queues
    voice = get(client.voice_clients, guild=ctx.guild)

    queues.clear()

    files = os.listdir()
    if 'Queue' in files:
        shutil.rmtree("./Queue")

    if voice and voice.is_playing():
        print("Music stopped")
        voice.stop()
        await ctx.send("Music stopped")
    else:
        print("No music playing failed to stop")
        await ctx.send("No music playing failed to stop")


@client.command(pass_context=True, aliases=['q', 'que'])
async def queue(ctx, url: str):
    global queues
    song_num = len(queues)
    song_name = f'queue{song_num}.mp3'
    files = os.listdir()

    if 'Queue' not in files:
        os.mkdir('Queue')

    ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'outtmpl': f'./Queue/{song_name}',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
    }

    queues[song_name] = ytsearch.title(url)

    try:
        if 'http' in url:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print("Downloading audio now\n")
                ydl.download([url])
        else:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print("Downloading audio now\n")
                ydl.download([ytsearch.main(url)])
    except:
        ctx.send('Invalid url/video title')

@client.command(pass_context=True, aliases=['n', 'nex'])
async def next(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Playing Next Song")
        voice.stop()
        await ctx.send("Next Song")
        next_song(ctx)
    else:
        print("No music playing")

@client.command(pass_context=True, aliases=['h'])
async def Help(ctx):
    embed = discord.Embed(
        title = 'Commands',
        description = 'Dj aatmann command list'
    )
    embed.add_field(name = 'Invite', value = 'join or ,j')
    embed.add_field(name = 'Remove', value = ',leave')
    embed.add_field(name = 'Play a song ▶', value = ',play')
    embed.add_field(name = 'Pause the song ⏸', value = ' ,pause')
    embed.add_field(name = 'Resume the song ⏯', value = ',r or ,resume')
    embed.add_field(name = 'Stopping the song ⏹', value = ',stop')

    await ctx.send(embed = embed)

TOKEN = os.environ('TOKEN')
client.run(TOKEN)

client.run('TOKEN')




