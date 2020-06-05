try:
    import discord
    from discord.ext import commands
    import youtube_dl
    from discord.voice_client import VoiceClient
    from discord.utils import get
    import shutil
    from os import system
    import os
    import ytsearch
    print('import complete')
except:
    raise FileNotFoundError

client = commands.Bot(command_prefix = '.')

players = {}

@client.event
async def on_ready():
    print('Bot is running')

@client.event
async def on_member_join(member):
    print(f'{member} joined')

@client.event
async def on_member_remove(member):
    print(f'{member} left')

@client.command(pass_context = True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()

@client.command(pass_context = True)
async def leave(ctx):
    await ctx.voice_client.disconnect()
    

@client.command(pass_context=True)
async def play(ctx, url: str):

    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07

            else:
                queues.clear()
                return

        else:
            queues.clear()



    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
    except PermissionError:
        await ctx.send("ERROR: Music playing")
        return


    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            shutil.rmtree(Queue_folder)

    await ctx.send("Getting everything ready now")

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        if 'http' in url:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        else:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([ytsearch.main(url)])

    except:
        c_path = os.path.dirname(os.path.realpath(__file__))
        system("spotdl -f " + '"' + c_path + '"' + " -s " + url)  # make sure there are spaces in the -s

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")


@client.command(pass_context=True)
async def pause(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        voice.pause()
        await ctx.send("Music paused")
    else:
        await ctx.send("Music not playing failed pause")


@client.command(pass_context=True)
async def resume(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        voice.resume()
        await ctx.send("Resumed music")


@client.command(pass_context=True)
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    queues.clear()

    if voice and voice.is_playing():
        voice.stop()
        await ctx.send("Music stopped")

queues = {}

@client.command(pass_context=True)
async def queue(ctx, url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except:
        q_path = os.path.abspath(os.path.realpath("Queue"))
        system(f"spotdl -ff song{q_num} -f " + '"' + q_path + '"' + " -s " + url)

    await ctx.send(f"Adding song {q_num} to the queue")


@client.command(pass_context=True)
async def next(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        voice.stop()
        await ctx.send("Next Song")

client.run('TOKEN')




