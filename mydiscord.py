# -------- Read Discord Messages -last updated 03/02/2021 by Steve Rogers
# ! python3
import logging
import os
import subprocess  # --- for launching external shell commands

import discord

import downloadbulletin  # --- my module for downloading the bulletin
import filelist  # --- definition of list of files and directories used in the proces
import getdatetime  # --- my module to get the current date / time
import maintainsong  # --- module to add a new song to OpenSong
import monitorfiles
import opensong  # --- my modulue to build the OpenSong set based on bulletin content and Discord postings
import utils
from utils import parse_songs_from_file, validate_songs

logging.basicConfig(level=logging.ERROR)

client = discord.Client()  # --- create and instance of the Discord client to connect to Discord
TOKEN = os.environ['DISCORD_TOKEN']
READ_CHANNEL = os.environ['READCHANNELID']
POST_CHANNEL = os.environ['POSTCHANNELID']


# print('MY TOKEN=', TOKEN)
# print('READ CHANNEL=', READ_CHANNEL)
# print('POST CHANNEL=', POST_CHANNEL)


# ------------ How to code a Discord Bot
# https://www.freecodecamp.org/news/create-a-discord-bot-with-python/

def read_discord(arg):
    print("\n !!!Hello world - OpenSong Discord Client starting at", getdatetime.currentdatetime())

    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))

        # --- display the current status
        # status_message = statuscheck()  # --- status message returned as a 'list' ***********

        # for x in status_message:  # --- print the status message
        #    print(x)

        status_message = monitorfiles.filechecker()  # --- status message returned as a 'string' ***********
        print(status_message)

    @client.event
    async def on_message(message):
        if message.author == client.user:  # --- don't respond to messages from yourself
            return ()

        msg = message.content  # --- retrieve the Discord message and process below
        print('\nDiscord Message received on channel:', message.channel, ' from ', message.author, ' on ',
              message.created_at, 'message =', msg, 'channel ID=', message.channel.id)

        # elif (message.channel.id == 681180782240464897):   #--- accept messages posted on the READ Channel

        if (message.channel.id == int(READ_CHANNEL)):  # --- accept messages posted on the READ Channel

            print('\nDiscord Message received on channel:', message.channel, ' from ', message.author, ' on ',
                  message.created_at)
            channel = client.get_channel(int(POST_CHANNEL))  # --- configure channel to receive reply messages

            # --- check the Discord message is for the Bulletin post -----
            if 'bulletinhasbeenposted' in msg.replace(" ", '').replace('\t', '').lower():
                status_message = 'Bulletin posted message received from ' + str(message.author) + ' on ' + str(
                    message.created_at)
                # post (status_message)
                await channel.send(status_message)

                # --- Download the bulletin which was just posted
                status_message = downloadbulletin.get_bulletin()
                # post (status_message)
                await channel.send(status_message)
            else:
                # --- write the Message to a file for later processingn
                textFile = open(filelist.DiscordMessageFilename, 'w', encoding='utf-8', errors='ignore')
                textFile.writelines(msg)
                textFile.close()

                # --- parse the incoming Discord message
                status_message = parsemessage()
                if 'Worship Schedule' in message.content:
                    # Create a list of songs from the text tile.
                    song_list = parse_songs_from_file(filelist.WorshipScheduleFilename)
                    # Check to see if the songs are valid.
                    invalid_songs = validate_songs(song_list, 5)

                    # Return a message on the song status
                    for message in invalid_songs['embed']:
                        await client.get_channel(int(READ_CHANNEL)).send(embed=invalid_songs['embed'][message])
                    # Apply any needed case-correction
                    utils.song_case_correction(filelist.WorshipScheduleFilename, song_list)

                if "Unrecognized" not in status_message:  # --- check if a valid status message was received
                    status_message = monitorfiles.filechecker()  # --- retrieve the current processing status
                    # status_message = statuscheck()  # --- Post the current status on the opensong channel
                    print(status_message)
                    await channel.send(status_message)
                else:
                    embed_data = discord.Embed(title="Unrecognized message", color=0xe74c3c,
                                               description="The entered command '" + message.content + "' was not "
                                                                                                       "recognized.")
                    embed_data.add_field(name="Time received:", value=message.created_at.strftime("%b %d %Y %H:%M:%S"),
                                         inline=True)
                    embed_data.add_field(name="User:", value=message.author, inline=True)
                    embed_data.add_field(name="The following messages are accepted",
                                         value="1. sermon info for *date* \n confession of sin for *date* \n "
                                               "assurance of "
                                               "pardon for *date* \n worship schedule for *date* \n Each message must "
                                               "be "
                                               "followed by the message content",
                                         inline=False)
                    await channel.send(embed=embed_data)

        # --only check for $commands on the "commands" channel
        elif message.channel.id == int(POST_CHANNEL):
            # --- check for the $status command -----
            if '/status' in msg.replace(" ", '').replace('\t', '').lower() or '$check' in msg.replace(" ", '').replace(
                    '\t', '').lower():
                print('\nDiscord Check Status message received from ', message.author, ' on ', message.created_at)
                status_message = monitorfiles.filechecker()  # ---read the current status message returned as a 'list'

                # --- post status message
                await message.channel.send(status_message)

                return ()

            # --- check for the $cleanup command used when processing did not complete successfully -----
            elif '/cleanup' in msg.replace(" ", '').replace('\t', '').lower() or '$check' in msg.replace(" ",
                                                                                                         '').replace(
                '\t', '').lower():
                print('\nDiscord Cleanup message received from ', message.author, ' on ', message.created_at)
                opensong.cleanup()  # ---cleanup residual files ******************************
                return ()

            # --- check for the $restore command message -----
            elif '/restore' in msg.replace(" ", '').replace('\t', '').lower():
                # print('\nOpenSong restore process message received from ', message.author, ' on ', message.created_at)
                restoreprocess()  # --- recover files to rerun the process *************************
                status_message = 'Discord restore processing completed'
                print('\nCurrent Status=', status_message)

                # --- post restore process completed message
                # await message.channel.send(status_message)
                status_message = monitorfiles.filechecker()  # --- status message returned as a 'string'

                # --- post status message
                print(status_message)
                return ()

            # --- check for the $update command -----
            elif '/update' in msg.replace(" ", '').replace('\t', '').lower():
                print('\nOpenSong update message received from ', message.author, ' on ', message.created_at)
                updateprocess()  # *************************************
                status_message = 'Discord Update processing completed'
                # print('\nCurrent Status=', status_message)

                # --- post rerun process completed message
                await message.channel.send(status_message)
                status_message = monitorfiles.filechecker()  # --- status message returned as a 'string'

                # --- post status message
                await message.channel.send(status_message)
                return ()

            # --- check for the $rerun command -----
            elif '/rerun' in msg.replace(" ", '').replace('\t', '').lower():
                print('\nOpenSong $rerun message received from ', message.author, ' on ', message.created_at)
                status_message = monitorfiles.filechecker()  # *************************************
                status_message = status_message + '$rerun processing completed!'
                print(status_message)

                return ()

            elif '/repost' in msg.lower():
                # --- split the command and parameters
                cmd = message.content.split()[0]
                # --- check if a parameter was passed
                if len(message.content.split()) > 1:
                    # --- get the message link as the parameter on the command
                    parameter = message.content.split()[1:]
                    parameter = parameter[0].strip("']")
                    # print('\nparameter=', parameter)

                    # --- break the https message link into a list of items;
                    items = str(parameter).split('/')
                    # for i in range(0, len(items)):
                    #    print(i, items[i])

                    server_id = int(items[4])
                    # --- retrive the channelID from the parsed message link
                    channel_id = int(items[5])
                    # --- retrieve the messageID from the parsed message link
                    message_id = int(items[6])

                    server = client.get_guild(server_id)
                    channel = server.get_channel(channel_id)
                    message_post = await channel.fetch_message(message_id)
                    message = message_post.content

                else:
                    status_message = '\nMissing Message link; message link is required'
                    await message.channel.send(status_message)
                    print(status_message)
                    return ()

                # print('\nMessage retrived', message.content)

                # --- write the Message to a file for later processingn
                textFile = open(filelist.DiscordMessageFilename, 'w', encoding='utf-8', errors='ignore')
                textFile.writelines(message)
                textFile.close()

                # --- parse the incoming Discord message
                status_message = parsemessage()
                # --- check if a valid status message was received
                if status_message:
                    # --- update the current processing status
                    status_message = monitorfiles.filechecker()

                status_message = status_message + '\nOpenSong  {} command received'.format(message)
                print(status_message)
                await channel.send(status_message)
                return ()

            # --- check for the $newsong command -----
            elif '/addsong' in msg.replace(" ", '').replace('\t', '').lower() or '$new' in msg.replace(" ", '').replace(
                    '\t', '').lower():
                message_text = message.content.replace('-', ' ').replace('<', '').replace('>', '')

                try:
                    # --- split the line at the first space to retrieve the song name
                    command, songname = message_text.split(' ', 1)
                    if message.attachments:  # --- check for attachments

                        # -- save the attachement
                        await message.attachments[0].save(filelist.NewSongTextFilename)
                        # --- call the addsong routine  ***********************************
                        status_message = maintainsong.addsong(songname)
                        # --- attempt to display the song which was just added
                        status_message = 'Use $search ' + songname + ' to display the song'
                        await message.channel.send(status_message)
                    else:
                        status_message = 'Missing file attachment with song lyrics!'
                        await message.channel.send(status_message)

                except ValueError:
                    status_message = 'Missing song name. Song name is required!'
                    await message.channel.send(status_message)

            # --- check for the $displaysong command -----
            elif '/displaysong' in msg.replace(" ", '').replace('\t', '').lower():
                status_text = '\nOpenSong  {} command received'.format(message.content)
                print(status_text)
                message_text = message.content
                if ' ' in message_text:
                    # --- split the line at the first space to retrieve the song name
                    command, song_name = message.content.split(' ',1)
                    print('\nSong name =', song_name)
                    song_matches = {}
                    # --- call the searchsong function
                    song_matches = utils.search_songs(song_name)

                    if len(song_matches) == 0:
                        status_message = '\nNo songs matching: {} found!)'.format(song_name)
                        # print(status_message)
                        await message.channel.send(status_message)
                    else:
                        for song, url in song_matches.items():
                            # print('\nsong:', song, 'url:', url)
                            embed = discord.Embed()
                            embed.description = '[' + song + '](' + url + ')'
                            status_message = embed.description
                            # --- post embed message
                            await message.channel.send(embed=embed)
                else:
                    status_message = '\nAt least a partial Song name is required for lookup'
                    await message.channel.send(status_message)

            elif '/displayset' in msg.replace(" ", '').replace('\t', '').lower():

                status_text = '\nOpenSong  {} command received'.format(message.content)
                print(status_text)
                set_matches = {}
                message_text = message.content

                if ' ' in message_text:
                    # --- split the line at the first space to retrieve the song name
                    command, set_date = message.content.split(' ',1)
                    print('\nInput Set Date =', set_date)

                    set_matches = maintainsong.displaySet(set_date)
                else:
                    set_date = str(getdatetime.nextSunday())  # --- set the default date of the next Sunday
                    set_matches = maintainsong.displaySet()  # --- call the DisplaySet function and use the default date ***********************

                if len(set_matches) == 0:
                    status_message = '\nNo sets matching: {} found!'.format(set_date)
                    # print(status_message)
                    await message.channel.send(status_message)
                else:
                    # print('\nSong {} Found)'. format(url))
                    # --- post returned URL
                    for myset, url in set_matches.items():
                        embed = discord.Embed()
                        embed.description = '[' + myset + '](' + url + ')'
                        status_message = embed.description
                        # --- post embed message
                        await message.channel.send(embed=embed)

                if len(set_matches) == 1:
                    returned_elements = maintainsong.bs4buildSetSummary(myset)
                    status_message = '\n'.join(returned_elements)  # --- convert list to string
                    print(status_message)
                    await message.channel.send(status_message)

            # --- check for the $help command -----
            elif '/help' in msg.replace(" ", '').replace('\t', '').lower():
                help_messages = ['The following commands are available ("$" is required):\n',
                                 '1. $status or $check\n',
                                 '2. $sync (forces sync from OpenSong to the gccpraise website\n',
                                 '3. $update (apply specific changes from a new post\n',
                                 '4. $addsong - <song name>\n',
                                 '5. $search <song name>\n',
                                 '6. $displayset <optional setDate in yyyy-mm-dd format>\n',
                                 '7. $help (to display this message)\n']
                # print('\nOpenSong Help command received from', message.author, ' on ', message.created_at)

                # --- post help message
                for x in help_messages:
                    await message.channel.send(x)
                return ()

            elif message.content.startswith('/hello'):
                await message.channel.send('Hello right back at you!')  # --- just for fun, reply to the same channel
                return

            # --- check for the $sync command (forces the rclone sync to the website -----
            elif '/sync' in msg.replace(" ", '').replace('\t', '').lower():
                # print('\nOpenSong Update Song message received from', message.author, ' on ', message.created_at)
                subprocess.Popen('/root/Dropbox/OpenSongV2/rclone-cron.sh')  # --- run the rclone sync process
                status_message = 'Discord Update Song <sync> processing completed'
                # print('\nCurrent Status=', status_message)

                # --- post Update Song process completed message
                await message.channel.send(status_message)

            elif msg.startswith('$'):
                channel = client.get_channel(opensong)
                reply_message = 'Unknown command received - no action taken'
                await message.channel.send(reply_message)
                message_author = str(message.author)
                reply_message = 'Message=', msg, ' received from:', message_author
                await message.channel.send(reply_message)
                reply_message = 'Use "$Help" for more information'
                await message.channel.send(reply_message)
                return

        return

    # --- Start the bot
    client.run(os.environ['DISCORD_TOKEN'])  # --- logon token retrieved from .env variable
    # --- End of Discord Bot


# --- Parse the incoming Discord message
def parsemessage():
    status_message = []
    valid_message = ''

    try:
        # --- Read the Discord message file
        textFile = open(filelist.DiscordMessageFilename, 'r', encoding='utf-8', errors='ignore')
        Lines = textFile.readlines()  # --- read the file into a list
        textFile.close()
    except:
        file_status = "Discord Message file {} does not exist. Unable to process messages...".format(filelist.DiscordMessageFilename)
        status_message.append(file_status)
        return (status_message)

    for i in range(0, len(Lines) - 1):
        # --- check for worship schedule message
        if 'worshipschedule' in Lines[i].replace(" ", '').replace('\t', '').lower():
            valid_message = 'true'
            worshipschedule = []
            status_message.append('Worship Schedule message received')
            for j in range(i, len(Lines)):
                line = Lines[j]
                worshipschedule.append(line)
                j += 1
            # --- write the worship schedule file
            textFile = open(filelist.WorshipScheduleFilename, 'w', encoding='utf-8', errors='ignore')
            textFile.writelines(worshipschedule)
            textFile.close()
            i = j  # --- reset the line pointer in the file

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

            # print('\nWorship Schedule file name is:', filelist.WorshipScheduleFilename)
            # --- write the Sermon Info file
            textFile = open(filelist.SermonInfoFilename, 'w', encoding='utf-8', errors='ignore')
            textFile.writelines(sermoninfo)
            textFile.close()
            i = j  # --- reset the line pointer in the file

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

            # --- write the Confession of Sin file
            textFile = open(filelist.ConfessionFilename, 'w', encoding='utf-8', errors='ignore')
            textFile.writelines(confessioninfo)
            textFile.close()
            i = j  # --- reset the line pointer in the file

        elif 'assuranceofpardon' in Lines[i].replace(" ", '').replace('\t', '').lower():
            valid_message = 'true'
            assuranceinfo = []
            status_message.append('Assurance of Pardon message received')

            for j in range(i, len(Lines)):
                line = Lines[j]
                # print('\nAof line: j=', j, ' line=', line, ' len=', len(Lines))
                assuranceinfo.append(line)
                if j + 1 == len(Lines):
                    break
                else:
                    if '@here' in Lines[j + 1]:
                        break
                j += 1

            # --- write the Assurance of Pardon
            textFile = open(filelist.AssuranceFilename, 'w', encoding='utf-8', errors='ignore')
            textFile.writelines(assuranceinfo)
            textFile.close()
            i = j  # --- reset the line pointer in the file

        i += 1
    if valid_message:
        return(status_message)  # --- if a valid message was posted, return status message as a list
    else:
        status_message.append('\nUnrecognized message received')
        return(status_message)


# ------------end of status checks

# ------------Start -  Re-run the OpenSong proces
def restoreprocess():
    # --- rename the previous processing files to prepare for re-running the process
    # --- Check if there is a new file first
    # --- rename the Old Assurance of Faith file
    # --- $restore command (execute the process build the set from the previous content) \n',
    print("\n !!!Warning -- this will overwrite any currently posted files!!! OpenSong restore processing starting at",
          getdatetime.currentdatetime())

    try:
        # --- rename the Old Assurance of Pardon of Sin file
        if os.path.isfile(filelist.OldAssuranceFilename):
            os.replace(filelist.OldAssuranceFilename, filelist.AssuranceFilename)
        else:
            print("Assurance of Pardon file {} does not exist. Assurance of Pardon must be manually posted...".format(
            filelist.OldAssuranceFilename))
    except:
            print("Assurance of Pardon file {} exists. Rename not performed...".format(
            filelist.OldAssuranceFilename))

    try:
        # --- rename the Old Confession of Sin file
        if os.path.isfile(filelist.ConfessionFilename):
            os.replace(filelist.OldConfessionFilename, filelist.ConfessionFilename)
        else:
            print("Confession of Sin file {} does not exist. Confession of Sin must be manually posted...".format(
            filelist.OldConfessionFilename))
    except:
            print("Confession of Sin file {} exists. Rename not performed...".format(
            filelist.OldConfessionFilename))

    try:
        # --- rename the Old Worship Schedule file
        if os.path.isfile(filelist.WorshipScheduleFilename):
            os.replace(filelist.OldWorshipScheduleFilename, filelist.WorshipScheduleFilename)
        else:
            print("Worship Schedule file {} does not exist. Worship Schedule must be manually posted...".format(
            filelist.OldWorshipScheduleFilename))
    except:
            print("Worship Schedule file {} exists. Rename not performed...".format(
            filelist.OldWorshipScheduleFilename))

    try:# --- rename the Old text Bulletin File
        if os.path.isfile(filelist.TextBulletinFilename):
            os.replace(filelist.OldTextBulletinFilename, filelist.TextBulletinFilename)
        else:
            print("Bulletin file {} does not exist. Bulletin posted message must be manually posted...".format(
            filelist.OldTextBulletinFilename))
    except:
            print("Bulletin file {} exists. Rename not performed...".format(
            filelist.OldTextBulletinFilename))

    # --- rerun the main process
    status_message = monitorfiles.filechecker()
    print(status_message)

    return (status_message)


# --- End of rerun processing

# ------------Start -  Re-run the OpenSong proces
def updateprocess():
    # --- Use the '$update' command to modify the content of  previous post for this week's processing
    # --- Check if there is a new file first; if there is, use it, otherwise use the archive file
    print("\n !!!OpenSong update processing starting at", getdatetime.currentdatetime())

    # --- read the bulletin date file
    textFile = open(filelist.BulletinDateFilename, 'r', encoding='utf-8', errors='ignore')
    bulletin_date = textFile.read()  # --- read the first line from the file
    textFile.close()

    # --- get current date
    current_date = getdatetime.currentdate()  # --- get today's date
    # --- parse the date from the bulletin date file
    returned_date = getdatetime.parsedates(bulletin_date)

    # --- compare dates
    if current_date > returned_date:  # --- Bulletin has already been processed
        print('\nCurrent Date ', current_date, ' is later than Bulletin date=', returned_date)
        monitorfiles.filechecker()  # --- continue with normal processing
        return ()
    else:
        print('\nBulletin Date ', bulletin_date, ' is later than Current Date=', current_date)

    if os.path.isfile(filelist.AssuranceFilename):  # --- new / updated file exists
        pass
    else:
        if os.path.isfile(filelist.OldAssuranceFilename):  # --- archive file exists and will be renamed to current
            os.replace(filelist.OldAssuranceFilename, filelist.AssuranceFilename)
        else:
            print("Assurance of Pardon file {} does not exist. Assurance of Faith must be posted...".format(
                filelist.OldAssuranceFilename))

    # --- check the Confession of Sin file
    if os.path.isfile(filelist.ConfessionFilename):
        pass
    else:
        if os.path.isfile(filelist.OldConfessionFilename):
            os.replace(filelist.OldConfessionFilename, filelist.ConfessionFilename)
        else:
            print("Confession of Sin file {} does not exist. Confession of Sin must be posted...".format(
                filelist.OldConfessionFilename))

    # --- Check the Worship Schedule file
    if os.path.isfile(filelist.WorshipScheduleFilename):
        pass
    else:
        if os.path.isfile(filelist.OldWorshipScheduleFilename):
            os.replace(filelist.OldWorshipScheduleFilename, filelist.WorshipScheduleFilename)
        else:
            print("Worship Schedule file {} does not exist. Worship Schedule must be posted...".format(
                filelist.OldWorshipScheduleFilename))

    # --- Check for the text Bulletin File
    if os.path.isfile(filelist.TextBulletinFilename):
        pass
    else:
        if os.path.isfile(filelist.OldTextBulletinFilename):
            os.replace(filelist.OldTextBulletinFilename, filelist.TextBulletinFilename)
        else:
            print("Bulletin file {} does not exist. New Bulletin text file must be posted...".format(
                filelist.OldTextBulletinFilename))

    # --- rerun the main process
    monitorfiles.filechecker()

    return ()


# --- End of rerun processing

def main():
    # ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
    print('\nNormal start - no argument provided')
    read_discord('normal')
    return ()

    # ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
    #
    if __name__ == "__main__":
        main()
#
# ======================================================================================
