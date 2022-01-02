# ----------------------------#
#     CONFIGURE LOGGING       #
# ----------------------------#
import logging
import logging.config
import os

import discord
from discord.ext import commands
from discord_slash import SlashCommand

import downloadbulletin
import filelist
import getdatetime
import maintainsong
import monitorfiles
import utils

# Create logging directory
if not os.path.exists('logs/'):
    os.makedirs('logs/')

# TODO: Add "Handlers=[]" argument to write to stdout and the file.
logging.basicConfig(filename='logs/debug.log',
                    level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] [%(filename)s] --> %(message)s",
                    datefmt='%m/%d/%Y %I:%M:%S %p')

# -------------------------#
#     SET CONSTANTS       #
# -------------------------#
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)
TOKEN = os.environ['DISCORD_TOKEN']
READ_CHANNEL = os.environ['READCHANNELID']
POST_CHANNEL = os.environ['POSTCHANNELID']
set_path = 'sets/'
bulletin_path = 'bulletin/'
VERSION = '2.09 - Belfast'


def read_discord():
    logging.info("Hello world - OpenSong Discord Client starting at" + getdatetime.currentdatetime())

    # -------------------------#
    #     Run once on start    #
    # -------------------------#
    @client.event
    async def on_ready():
        logging.info('We have logged in as {0.user}'.format(client))

    # -----------------------------------#
    #     Run on each message received   #
    # -----------------------------------#
    @client.event
    async def on_message(message):
        if message.author == client.user:  # don't respond to messages from yourself
            return ()

        msg = message.content  # retrieve the Discord message and process below
        print('Discord Message received on channel:', message.channel, ' from ', message.author, ' on ',
              message.created_at)
        channel = client.get_channel(int(POST_CHANNEL))  # --- configure channel to receive reply messages

        if message.channel.id == int(READ_CHANNEL):  # --- accept messages posted on the READ Channel

            print('Discord Message received on channel:', message.channel, ' from ', message.author, ' on ',
                  message.created_at)
            channel = client.get_channel(int(POST_CHANNEL))  # --- configure channel to receive reply messages

            # check the Discord message is for the Bulletin post -----
            if "bulletinhasbeenposted" in msg.replace(" ", '').replace('\t', '').lower():
                # Download the bulletin which was just posted
                logging.info(downloadbulletin.get_bulletin())
                await message.channel.send(embed=utils.status_embed("bulletin", message))
                status_message = monitorfiles.statuscheck()  # retrieve the current processing status

                if 'Set processing completed' in status_message:
                    embed_data = discord.Embed(title="Set Status", color=0x2ECC71,
                                               description="OpenSong Set Processing")
                    embed_data.add_field(name="Status:", value=status_message, inline=True)
                    await client.get_channel(int(READ_CHANNEL)).send(embed=embed_data)

                    # --- call the DisplaySet function to display the set
                    split_string = status_message.split('\n')  # --- break up the message
                    set_name = split_string[1]  # --- extract the set name from the message
                    set_name = set_name.replace(' for: ', '')
                    set_url = maintainsong.displaySet(set_name)

                    content = ""
                    set_summary = maintainsong.bs4buildSetSummary(set_name)  # --- build the set summary
                    content = content + "\n" + "[" + set_name + "]" + "(" + set_url + ")"

                    content = content + '\n' + set_summary

                    embed_data = discord.Embed(title="Found " + set_name + ".",
                                               description=content)
                    await message.channel.send(embed=embed_data)
            else:
                #  write the Message to a file for later processing
                textFile = open(bulletin_path + filelist.DiscordMessageFilename, 'w', encoding='utf-8', errors='ignore')
                textFile.writelines(msg)
                textFile.close()

                # --- parse the incoming Discord message
                status_message = utils.parsemessage()

                if 'Worship Schedule' in message.content:
                    # Create a list of songs from the text tile.
                    song_list = utils.parse_songs_from_file(bulletin_path + filelist.WorshipScheduleFilename)
                    if type(song_list) != str:
                        # Check to see if the songs are valid.
                        invalid_songs = utils.validate_songs(song_list, 5)

                        # Return a message on the song status
                        for return_message in invalid_songs['embed']:
                            await client.get_channel(int(READ_CHANNEL)) \
                                .send(embed=invalid_songs['embed'][return_message])
                        # Apply any needed case-correction - must pass in the song_list of correct case.
                        utils.song_case_correction(bulletin_path + filelist.WorshipScheduleFilename,
                                                   invalid_songs['songs'])

                    else:
                        logging.error("not able to validate any songs in the worship schedule.")
                        embed_data = discord.Embed(title="Error!", color=0x2ECC71,
                                                   description="There were not any songs found in the worship schedule."
                                                               "Please ensure the formatting is correct and post"
                                                               "the message again.")
                        await message.channel.send(embed=embed_data)

                if 'sermon info' in message.content:
                    await message.channel.send(embed=utils.status_embed("sermon info", message))
                if 'confession of sin' in message.content:
                    await message.channel.send(embed=utils.status_embed("confession of sin", message))

                if 'assurance of pardon' in message.content:
                    await message.channel.send(embed=utils.status_embed("assurance of pardon", message))

                if "Unrecognized" not in status_message:  # --- check if a valid status message was received
                    monitorfiles.set_cleanup(cleanup_type='set')  # --- delete the set before processing

                    status_message = monitorfiles.statuscheck()  # retrieve the current processing status

                    # if 'Set processing completed' in status_message:
                    if 'processing completed' in status_message:
                        embed_data = discord.Embed(title="Set Status", color=0x2ECC71,
                                                   description="OpenSong Set Processing")
                        embed_data.add_field(name="Status:", value=status_message, inline=True)
                        await client.get_channel(int(READ_CHANNEL)).send(embed=embed_data)

                        # --- call the DisplaySet function to display the set
                        split_string = status_message.split('\n')  # --- break up the message
                        set_name = split_string[1]  # --- extract the set name from the message
                        set_name = set_name.replace(' for: ', '')
                        set_url = maintainsong.displaySet(set_name)

                        content = ""
                        set_summary = maintainsong.bs4buildSetSummary(set_name)  # --- build the set summary
                        content = content + "\n" + "[" + set_name + "]" + "(" + set_url + ")"
                        content = content + '\n' + set_summary

                        embed_data = discord.Embed(title="Found " + set_name + ".",
                                                   description=content)
                        await message.channel.send(embed=embed_data)

                    # await channel.send(embed=utils.convert_embed(status_message))

                # --- check if a valid status message was received
                elif status_message:
                    status_message = monitorfiles.filechecker()

                    status_message = "{0}{1}".format(status_message, '\nOpenSong  {} command received'.format(message))
                    print(status_message)
                    await channel.send(utils.convert_embed(status_message))
        await client.process_commands(message)

    # -----------------------------------#
    #     Process Bot Commands           #
    # -----------------------------------#

    @slash.slash(name="ping")
    async def ping(ctx):
        await ctx.send(f"Pong! ({client.latency * 1000}ms)")

    @slash.slash(name="hello")
    async def hello(ctx):
        await ctx.send("Hello right back at you!")

    @slash.slash(name="file", description="Shows the text of the given file.")
    async def show_file(ctx, filename):
        try:
            # Only allow the subdirectory of logs.
            if filename.startswith("logs/"):
                file = discord.File(filename)
                await ctx.send(file=file)

            # If any other directory tries to get accessed give an error.
            elif not filename.find('/'):
                logging.warning("Directory Traversal Detected!")
                embed = discord.Embed(title="Error! ", color=discord.Colour.red(),
                                      description="Please enter a valid filename. (Example: mydiscord.py")
                await ctx.send(embed=embed)
            else:
                file = discord.File(filename)
                await ctx.send(file=file)
        except Exception as e:
            logging.warning(e)
            embed = discord.Embed(title="Exception Error!", description=e)
            await ctx.send(embed=embed)

    @slash.slash(
        name="status",
        description="Displays the status of the build process for this weeks set")
    async def status(ctx):
        # await ctx.send(embed=utils.convert_embed(monitorfiles.statuscheck()))
        status_message = monitorfiles.statuscheck()
        if 'Set processing completed' in status_message:
            embed_data = discord.Embed(title="Set Status", color=0x2ECC71,
                                       description="OpenSong Set Processing")
            embed_data.add_field(name="Status:", value=status_message, inline=True)
            await client.get_channel(int(READ_CHANNEL)).send(embed=embed_data)

            # --- call the DisplaySet function to display the set
            split_string = status_message.split('\n')  # --- break up the message
            set_name = split_string[1]  # --- extract the set name from the message
            set_name = set_name.replace(' for: ', '')
            set_url = maintainsong.displaySet(set_name)

            content = ""
            set_summary = maintainsong.bs4buildSetSummary(set_name)  # --- build the set summary
            content = content + "\n" + "[" + set_name + "]" + "(" + set_url + ")"

            content = content + '\n' + set_summary

            embed_data = discord.Embed(title="Found " + set_name + " .",
                                       description=content)
            await ctx.send(embed=embed_data)

        else:
            await ctx.send(status_message)

    @slash.slash(name="cleanup", description="Removes files from the bulletin directory")
    async def cleanup(ctx):
        await ctx.send(embed=utils.convert_embed(monitorfiles.cleanup()))

    @slash.slash(
        name="rerun",
        description="Triggers the set build and displays the current status."
    )
    async def rerun(ctx):
        await ctx.send(embed=utils.convert_embed(monitorfiles.filechecker()))

    @slash.slash(
        name="set-cleanup",
        description="Deletes bulletin files and the set file."
    )
    async def set_cleanup(ctx):
        await ctx.send(embed=utils.convert_embed(monitorfiles.set_cleanup()))

    @slash.slash(
        name="version",
        description="displays the current bot version."
    )
    async def version(ctx):
        await ctx.send("OpenSong Discord Version " + VERSION)

    @slash.slash(
        name="repost-message",
        description="Reposts the message with the given ID"
    )
    async def repost(ctx, message_id):
        msg = await ctx.channel.fetch_message(int(message_id))
        await ctx.send(msg)

    @slash.slash(
        name="add-song",
        description="Updates the song index on the gccpraise.com website"
    )
    async def add_song(ctx, song_name):
        status_message = maintainsong.addsong(song_name)  # --- validates song against Dropbox
        if 'no matching song found' in status_message:
            embed_data = discord.Embed(title="Song Not Found: " + song_name,
                                       description='no matching song found')
            await ctx.send(embed=embed_data)
            return ()

        else:
            song_matches = utils.search_songs(song_name)  # --- validate song name against website
            content = ""
            for song in song_matches:
                content = content + "\n" + "[" + song + "]" + "(" + song_matches[song] + ")"
                song_name = song

            if len(song_matches) == 1:  # --- found exact match
                status_message = maintainsong.dropbox_website_sync(song_name)

                embed_data = discord.Embed(title="Update Song ",
                                           description=content)
                await ctx.send(embed=embed_data)
            else:
                embed_data = discord.Embed(
                    title="Found " + str(len(song_matches)) + " possible matche(s) for song: " + song_name,
                    description=content)
                await ctx.send(embed=embed_data)

    @slash.slash(
        name="update-song",
        description="Updates the song index on the gccpraise.com website "
    )
    async def update_song(ctx, song_name):
        song_matches = utils.search_songs(song_name)  # --- validate song name against website
        content = ""
        for song in song_matches:
            content = content + "\n" + "[" + song + "]" + "(" + song_matches[song] + ")"

        if len(song_matches) == 1 or song_name in song_matches:  # --- found exact match
            status_message = maintainsong.dropbox_website_sync(song_name)
            content = ""
            content = content + "\n" + "[" + song_name + "]" + "(" + song_matches[song_name] + ")"
            embed_data = discord.Embed(title="Update Song: " + song_name,
                                       description=content)
            await ctx.send(embed=embed_data)
        else:
            for song in song_matches:
                content = content + "\n" + "[" + song + "]" + "(" + song_matches[song] + ")"
                # song_name = song
            embed_data = discord.Embed(
                title="Found " + str(len(song_matches)) + " possible matche(s) for song: " + song_name,
                description=content)
            await ctx.send(embed=embed_data)

    @slash.slash(
        name="display-song",
        description="Retrieves a song from the website"
    )
    async def display_song(ctx, song_name):
        song_matches = utils.search_songs(song_name)
        content = ""
        for song in song_matches:
            content = content + "\n" + "[" + song + "]" + "(" + song_matches[song] + ")"
        embed_data = discord.Embed(
            title="Found " + str(len(song_matches)) + " possible matche(s) for song: " + song_name,
            description=content)
        await ctx.send(embed=embed_data)

    @slash.slash(
        name="display-set",
        description="Retrieves a set from the website"
    )
    async def display_set(ctx):
        set_url = "https://gccpraise.com/preview_set.php"
        content = ""
        content = content + "\n" + "(" + set_url + ")"

        embed_data = discord.Embed(title="Display Set!",
                                   description=content)
        await ctx.send(embed=embed_data)

    # -----------------------------------#
    #     Start the discord bot.         #
    # -----------------------------------#
    # client.run(os.environ['DISCORD_TOKEN'])

    # --- Start the bot
    client.run(os.environ['DISCORD_TOKEN'])  # --- logon token retrieved from .env variable
    # --- End of Discord Bot


# ------------end of status checks

# -----------------------------------#
#     Main Routine Call              #
# -----------------------------------#
def main():
    read_discord()
    return ()
