import logging
import os

import discord
from discord.ext import commands
from discord_slash import SlashCommand

import downloadbulletin
import filelist
import getdatetime
import maintainsong
import monitorfiles
import readworshipschedule
import utils

# -------------------------#
#     SET CONSTANTS       #
# -------------------------#
logging.basicConfig(level=logging.INFO)
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)
TOKEN = os.environ['DISCORD_TOKEN']
READ_CHANNEL = os.environ['READCHANNELID']
POST_CHANNEL = os.environ['POSTCHANNELID']
set_path = 'sets/'
bulletin_path = 'bulletin/'
VERSION = '1.03'


def read_discord():
    logging.info("\n !!!Hello world - OpenSong Discord Client starting at", getdatetime.currentdatetime())

    # -------------------------#
    #     Run once on start    #
    # -------------------------#
    @client.event
    async def on_ready():
        logging.info('We have logged in as {0.user}'.format(client))

    # TODO: uncomment the below line.
    # if os.environ['ENVIRON'] == 'DEV':
    # --- call the test / validation script as the first thing before the bot starts

    #    startup_validation.run_test_scripts()

    # -----------------------------------#
    #     Run on each message received   #
    # -----------------------------------#
    @client.event
    async def on_message(message):        
        if message.author == client.user:  # don't respond to messages from yourself
            return ()

        msg = message.content  # retrieve the Discord message and process below
        logging.info('Discord Message received on channel:', message.channel, ' from ', message.author, ' on ',
                     message.created_at, 'message =', msg, 'channel ID=', message.channel.id)

        if message.channel.id == int(READ_CHANNEL):  # --- accept messages posted on the READ Channel

            logging.info('Discord Message received on channel:', message.channel, ' from ', message.author, ' on ',
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
                    # --- call the DisplaySet function and use the default date ***********************
                    set_matches = maintainsong.displaySet()

                    if len(set_matches) == 0:
                        set_date = str(getdatetime.nextSunday())  # --- set the default date of the next Sunday

                        status_message = '\nNo sets matching: {} found!'.format(set_date)
                        await message.channel.send(status_message)
                    else:
                        for my_set, url in set_matches.items():
                            embed = discord.Embed()
                            embed.description = '[' + my_set + '](' + url + ')'
                            status_message = embed.description
                            # --- post embed message
                            await message.channel.send(embed=embed)

            else:
                #  write the Message to a file for later processing
                textFile = open(bulletin_path + filelist.DiscordMessageFilename, 'w', encoding='utf-8', errors='ignore')
                textFile.writelines(msg)
                textFile.close()

                #  parse the incoming Discord message
                status_message = parse_message()
                if 'Worship Schedule' in message.content:
                    # Create a list of songs from the text tile.
                    song_list = utils.parse_songs_from_file(bulletin_path + filelist.WorshipScheduleFilename)
                    # Check to see if the songs are valid.
                    invalid_songs = utils.validate_songs(song_list, 5)

                    # Return a message on the song status
                    for return_message in invalid_songs['embed']:
                        await client.get_channel(int(READ_CHANNEL)).send(embed=invalid_songs['embed'][return_message])
                    # Apply any needed case-correction - must pass in the song_list of correct case.
                    utils.song_case_correction(bulletin_path + filelist.WorshipScheduleFilename, invalid_songs['songs'])

                if 'sermon info' in message.content:
                    await message.channel.send(embed=utils.status_embed("sermon info", message))
                if 'confession of sin' in message.content:
                    await message.channel.send(embed=utils.status_embed("confession of sin", message))
                    
                if 'assurance of pardon' in message.content:
                    await message.channel.send(embed=utils.status_embed("assurance of pardon", message))
                    
                if "Unrecognized" not in status_message:  # --- check if a valid status message was received
                    status_message = monitorfiles.statuscheck()  # --- retrieve the current processing status
                    # status_message = statuscheck()  # --- Post the current status on the opensong channel
                    logging.info(status_message)
                    await channel.send(status_message)
                    if 'Set processing completed' in status_message:
                        embed_data = discord.Embed(title="Set Status", color=0x2ECC71,
                                                   description="OpenSong Set Processing")
                        embed_data.add_field(name="Status:", value=status_message, inline=True)
                        await client.get_channel(int(READ_CHANNEL)).send(embed=embed_data)
                        set_matches = maintainsong.displaySet()
                        if len(set_matches) == 0:
                            set_date = str(getdatetime.nextSunday())  # --- set the default date of the next Sunday
                            status_message = '\nNo sets matching: {} found!'.format(set_date)
                            await message.channel.send(status_message)
                        else:
                            for my_set, url in set_matches.items():
                                embed = discord.Embed()
                                embed.description = '[' + my_set + '](' + url + ')'
                                # --- post embed message
                                await message.channel.send(embed=embed)

                textFile = open(bulletin_path + filelist.DiscordMessageFilename, 'w', encoding='utf-8', errors='ignore')
                textFile.writelines(message)
                textFile.close()
                status_message = parse_message()
                if status_message:
                    status_message = monitorfiles.filechecker()
                status_message = status_message + '\nOpenSong  {} command received'.format(message)
                logging.info(status_message)
                await channel.send(utils.convert_embed(status_message))
        await client.process_commands(message)

    # -----------------------------------#
    #     Process Bot Commands           #
    # -----------------------------------#

    # TODO: Figure out if this needs to be calculated each run from the server the bots in.
    guild_ids = [841103547924086844]  # Put your server ID in this array.

    @slash.slash(name="ping", guild_ids=guild_ids)
    async def ping(ctx):
        await ctx.send(f"Pong! ({client.latency * 1000}ms)")

    @slash.slash(name="hello", guild_ids=guild_ids)
    async def hello(ctx):
        await ctx.send("Hello right back at you!")

    @slash.slash(name="file", guild_ids=guild_ids, description="Shows the text of the given file.")
    async def show_file(ctx, filename):
        try:
            file = discord.File(filename)
            await ctx.send(file=file)
        except Exception as e:
            embed = discord.Embed(title="Exception Error!", description=e)
            await ctx.send(embed=embed)

    @slash.slash(name="cleanup", guild_ids=guild_ids, description="Removes files from the bulletin directory")
    async def cleanup(ctx):
        await ctx.send(embed=utils.convert_embed(monitorfiles.cleanup()))

    @slash.slash(
        name="rerun",
        guild_ids=guild_ids,
        description="Triggers the set build and displays the current status."
    )
    async def rerun(ctx):
        await ctx.send(embed=utils.convert_embed(monitorfiles.filechecker()))

    @slash.slash(
        name="set-cleanup",
        guild_ids=guild_ids,
        description="Deletes bulletin files and the set file."
    )
    async def set_cleanup(ctx):
        await ctx.send(embed=utils.convert_embed(monitorfiles.set_cleanup()))

    @slash.slash(
        name="version",
        guild_ids=guild_ids,
        description="displays the current bot version."
    )
    async def version(ctx):
        await ctx.send("OpenSong Discord Version " + VERSION)

    @slash.slash(
        name="repost-message",
        guild_ids=guild_ids,
        description="Reposts the message with the given ID"
    )
    async def repost(ctx, message_id):
        msg = await ctx.fetch_message(message_id)
        await ctx.send(msg)

    @slash.slash(
        name="add-song",
        guild_ids=guild_ids,
        description="Adds a song the website and dropbox with attached "
                    "song.txt"
    )
    async def add_song(ctx):
        await ctx.send("This command has not been implemented yet."
                       )

    @slash.slash(
        name="display-song",
        guild_ids=guild_ids,
        description="Retrieves a song from the website"
    )
    async def display_song(ctx):
        await ctx.send("This command has not been implemented yet."
                       )

    @slash.slash(
        name="display-set",
        guild_ids=guild_ids,
        description="Retrieves a set from the website"
    )
    async def display_set(ctx):
        await ctx.send("This command has not been implemented yet."
                       )

    @slash.slash(
        name="sync",
        guild_ids=guild_ids,
        description="Description needed..."
    )
    async def sync(ctx):
        await ctx.send("This command has not been implemented yet.")

    # -----------------------------------#
    #     Start the discord bot.         #
    # -----------------------------------#
    client.run(os.environ['DISCORD_TOKEN'])


def parse_message():
    status_message: list[str] = []
    valid_message = ''

    try:
        # --- Read the Discord message file
        textFile = open(bulletin_path + filelist.DiscordMessageFilename, 'r', encoding='utf-8', errors='ignore')
        Lines = textFile.readlines()  # --- read the file into a list
        textFile.close()
        # TODO: Scope this exception (PEP 8: E722 do not use bare 'except')
    except:
        file_status = "Discord Message file {} does not exist. Unable to process messages...".format(
            bulletin_path + filelist.DiscordMessageFilename)
        status_message.append(file_status)
        return status_message

    # TODO: Rewrite these into a singular function, removing magic numbers.
    # https://en.wikipedia.org/wiki/Magic_number_%28programming%29#Unnamed_numerical_constants
    for i in range(0, len(Lines) - 1):
        # --- check for worship schedule message
        if 'worshipschedule' in Lines[i].replace(" ", '').replace('\t', '').lower():
            valid_message = 'true'
            worship_schedule = []
            status_message.append('Worship Schedule message received')
            for j in range(i, len(Lines)):
                line = Lines[j]
                worship_schedule.append(line)
                j += 1
            # --- write the worship schedule file
            textFile = open(bulletin_path + filelist.WorshipScheduleFilename, 'w', encoding='utf-8', errors='ignore')
            textFile.writelines(worship_schedule)
            textFile.close()
            # reset the line pointer in the file
            i = j

            # read the worship schedule file extracted from discord and store in a  "lists" file
            readworshipschedule.readWS()

        elif 'sermoninfo' in Lines[i].replace(" ", '').replace('\t', '').lower():
            valid_message = 'true'
            sermoninfo = []
            status_message.append('Sermon Info message received')
            for j in range(i, len(Lines)):
                line = Lines[j]
                sermoninfo.append(line)
                if j + 1 == len(Lines):
                    break
                else:
                    if '@here' in Lines[j + 1]:
                        break
                j += 1

            # --- write the Sermon Info file
            textFile = open(bulletin_path + filelist.SermonInfoFilename, 'w', encoding='utf-8', errors='ignore')
            textFile.writelines(sermoninfo)
            textFile.close()
            # reset the line pointer in the file
            i = j

        elif 'confessionofsin' in Lines[i].replace(" ", '').replace('\t', '').lower():
            valid_message = 'true'
            confessioninfo = []
            status_message.append('Confession of Sin message received')

            for j in range(i, len(Lines)):
                line = Lines[j]
                confessioninfo.append(line)
                if j + 1 == len(Lines):
                    break
                else:
                    if '@here' in Lines[j + 1]:
                        break
                j += 1

            # write the Confession of Sin file
            textFile = open(bulletin_path + filelist.ConfessionFilename, 'w', encoding='utf-8', errors='ignore')
            textFile.writelines(confessioninfo)
            textFile.close()
            # reset the line pointer in the file
            i = j

        elif 'assuranceofpardon' in Lines[i].replace(" ", '').replace('\t', '').lower():
            valid_message = 'true'
            assuranceinfo = []
            status_message.append('Assurance of Pardon message received')

            for j in range(i, len(Lines)):
                line = Lines[j]
                assuranceinfo.append(line)
                if j + 1 == len(Lines):
                    break
                else:
                    if '@here' in Lines[j + 1]:
                        break
                j += 1

            # write the Assurance of Pardon
            textFile = open(bulletin_path + filelist.AssuranceFilename, 'w', encoding='utf-8', errors='ignore')
            textFile.writelines(assuranceinfo)
            textFile.close()
            # reset the line pointer in the file
            i = j

        i += 1
    if valid_message:
        return status_message
    else:
        status_message.append('\nUnrecognized message received')
        return status_message

    # ----------------------------#
    #     Start the Bot           #
    # ----------------------------#


# -----------------------------------#
#     Main Routine Call              #
# -----------------------------------#
def main():
    read_discord()
    return ()
