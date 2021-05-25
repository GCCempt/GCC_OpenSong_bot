# -------- Read Discord Messages -last updated 03/02/2021 by Steve Rogers
# ! python3
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
import pandas as pd  # Python data analysis library
import logging
import startup_validation 
import readworshipschedule
logging.basicConfig(level=logging.ERROR)

client = discord.Client()  # --- create and instance of the Discord client to connect to Discord
TOKEN = os.environ['DISCORD_TOKEN']
READ_CHANNEL = os.environ['READCHANNELID']
POST_CHANNEL = os.environ['POSTCHANNELID']

set_path = 'sets/'
bulletin_path = 'bulletin/'

# print('MY TOKEN=', TOKEN)
# print('READ CHANNEL=', READ_CHANNEL)
# print('POST CHANNEL=', POST_CHANNEL)


# ------------ How to code a Discord Bot
# https://www.freecodecamp.org/news/create-a-discord-bot-with-python/

def read_discord():
    print("\n !!!Hello world - OpenSong Discord Client starting at", getdatetime.currentdatetime())

    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))

    if os.environ['ENVIRON'] == 'DEV':
            # --- call the test / validation script as the first thing before the bot starts
        startup_validation.run_test_scripts()

    @client.event
    async def on_message(message):
        if message.author == client.user:  # --- don't respond to messages from yourself
            return ()

        msg = message.content  # --- retrieve the Discord message and process below
        print('\nDiscord Message received on channel:', message.channel, ' from ', message.author, ' on ',
              message.created_at, 'message =', msg, 'channel ID=', message.channel.id)
     
        if (message.channel.id == int(READ_CHANNEL)):  # --- accept messages posted on the READ Channel

            print('\nDiscord Message received on channel:', message.channel, ' from ', message.author, ' on ',
                  message.created_at)
            channel = client.get_channel(int(POST_CHANNEL))  # --- configure channel to receive reply messages

            # --- check the Discord message is for the Bulletin post -----
            if 'bulletinhasbeenposted' in msg.replace(" ", '').replace('\t', '').lower():
                status_message = 'Bulletin information received successfully!' + str(message.author) + ' on ' + str(
                    message.created_at)
 
                # --- Download the bulletin which was just posted
                status_message = status_message + downloadbulletin.get_bulletin()
                print(status_message)
                
                embed_data = discord.Embed(title="Bulletin", color=0x2ECC71,
                                               description="Bulletin info posted successfully.")
                embed_data.add_field(name="Time received:", value=message.created_at.strftime("%b %d %Y %H:%M:%S"),
                                         inline=True)
                embed_data.add_field(name="User:", value=message.author, inline=True)
                await client.get_channel(int(READ_CHANNEL)).send(embed=embed_data)

                status_message = monitorfiles.statuscheck()  # --- retrieve the current processing status
                
                if 'Set processing completed' in status_message:
                    embed_data = discord.Embed(title="Set Status", color=0x2ECC71,
                                               description="OpenSong Set Processing")
                    embed_data.add_field(name="Status:", value=status_message, inline=True)
                    await client.get_channel(int(READ_CHANNEL)).send(embed=embed_data)

                    set_matches = maintainsong.displaySet()  # --- call the DisplaySet function and use the default date ***********************

                    if len(set_matches) == 0:
                        set_date = str(getdatetime.nextSunday())  # --- set the default date of the next Sunday

                        status_message = '\nNo sets matching: {} found!'.format(set_date)
                        await message.channel.send(status_message)
                    else:
                        for myset, url in set_matches.items():
                            embed = discord.Embed()
                            embed.description = '[' + myset + '](' + url + ')'
                            status_message = embed.description
                            # --- post embed message
                            await message.channel.send(embed=embed)

            else:
                # --- write the Message to a file for later processingn
                textFile = open(bulletin_path + filelist.DiscordMessageFilename, 'w', encoding='utf-8', errors='ignore')
                textFile.writelines(msg)
                textFile.close()

                # --- parse the incoming Discord message
                status_message = utils.parsemessage()
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
                    embed_data = discord.Embed(title="Sermon", color=0x2ECC71,
                                               description="Sermon info received successfully.")
                    embed_data.add_field(name="Time received:", value=message.created_at.strftime("%b %d %Y %H:%M:%S"),
                                         inline=True)
                    embed_data.add_field(name="User:", value=message.author, inline=True)
                    await client.get_channel(int(READ_CHANNEL)).send(embed=embed_data)

                if 'confession of sin' in message.content:
                    embed_data = discord.Embed(title="Confession", color=0x2ECC71,
                                               description="Confession of sin received successfully.")
                    embed_data.add_field(name="Time received:", value=message.created_at.strftime("%b %d %Y %H:%M:%S"),
                                         inline=True)
                    embed_data.add_field(name="User:", value=message.author, inline=True)
                    await client.get_channel(int(READ_CHANNEL)).send(embed=embed_data)

                if 'assurance of pardon' in message.content:
                    embed_data = discord.Embed(title="Assurance", color=0x2ECC71,
                                               description="Assurance of pardon received successfully.")
                    embed_data.add_field(name="Time received:", value=message.created_at.strftime("%b %d %Y %H:%M:%S"),
                                         inline=True)
                    embed_data.add_field(name="User:", value=message.author, inline=True)
                    await client.get_channel(int(READ_CHANNEL)).send(embed=embed_data)

                if "Unrecognized" not in status_message:  # --- check if a valid status message was received
                    status_message = monitorfiles.statuscheck()  # --- retrieve the current processing status
                    # status_message = statuscheck()  # --- Post the current status on the opensong channel
                    print(status_message)
                    await channel.send(status_message)

                    if 'Set processing completed' in status_message:
                        embed_data = discord.Embed(title="Set Status", color=0x2ECC71,
                                               description="OpenSong Set Processing")
                        embed_data.add_field(name="Status:", value=status_message, inline=True)
                        await client.get_channel(int(READ_CHANNEL)).send(embed=embed_data)

                        set_matches = maintainsong.displaySet()  # --- call the DisplaySet function and use the default date ***********************

                        if len(set_matches) == 0:
                            set_date = str(getdatetime.nextSunday())  # --- set the default date of the next Sunday

                            status_message = '\nNo sets matching: {} found!'.format(set_date)
                            await message.channel.send(status_message)
                        else:
                            for myset, url in set_matches.items():
                                embed = discord.Embed()
                                embed.description = '[' + myset + '](' + url + ')'
                                status_message = embed.description
                                # --- post embed message
                                await message.channel.send(embed=embed)

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

        # --only check for /commands on the "commands" channel
        elif message.channel.id == int(POST_CHANNEL):
            # --- check for the /status command -----
            if '/status' in msg.replace(" ", '').replace('\t', '').lower() or '/check' in msg.replace(" ", '').replace(
                    '\t', '').lower():
                print('\nDiscord Check Status message received from ', message.author, ' on ', message.created_at)
                status_message = monitorfiles.statuscheck()  # ---read the current status message returned as a 'list'
 
                # --- post status message
                #await message.channel.send(status_message)
                embed_data = discord.Embed(title="Build Set Status", color=0x2ECC71,
                                    description="OpenSong Set Build Progress")
                embed_data.add_field(name="Status:", value=status_message, inline=True)
                await client.get_channel(int(POST_CHANNEL)).send(embed=embed_data)

                return ()

            # --- check for the /cleanup command used when processing did not complete successfully -----
            elif '/cleanup' in msg.replace(" ", '').replace('\t', '').lower() or '/check' in msg.replace(" ",
                                                                                                         '').replace(
                '\t', '').lower():
                print('\nDiscord Cleanup message received from ', message.author, ' on ', message.created_at)
                status_message = monitorfiles.cleanup()  # ---cleanup residual files ******************************

                # --- post status message
                await message.channel.send(status_message)
                return ()

            # --- check for the /rerun command -----
            elif '/rerun' in msg.replace(" ", '').replace('\t', '').lower():
                print('\nOpenSong /rerun message received from ', message.author, ' on ', message.created_at)
                status_message = monitorfiles.filechecker()  # *************************************
                status_message = status_message + '/rerun processing completed!'
                print(status_message)

                return ()

            elif '/setcleanup' in msg.replace(" ", '').replace('\t', '').lower() or '/check' in msg.replace(" ",
                                                                                                         '').replace(
                '\t', '').lower():
                print('\nDiscord Set Cleanup message received from ', message.author, ' on ', message.created_at)
                status_message = monitorfiles.set_cleanup()  # ---cleanup set in DEV environment ******************************
                
                # --- post status message
                await message.channel.send(status_message)
                return ()

            elif '/version' in msg.replace(" ", '').replace('\t', '').lower() or '/check' in msg.replace(" ",
                                                                                                         '').replace(
                '\t', '').lower():
                status_message = '\nOpenSong Discord Version 1.03\n'
                 
                # --- post status message
                await message.channel.send(status_message)
                return ()
            # --- check for the /rerun command -----
            elif '/rerun' in msg.replace(" ", '').replace('\t', '').lower():
                print('\nOpenSong /rerun message received from ', message.author, ' on ', message.created_at)
                status_message = monitorfiles.filechecker()  # *************************************
                status_message = status_message + '/rerun processing completed!'
                print(status_message)

                return ()

            # --- check for the /validate command -----
            elif '/validate' in msg.replace(" ", '').replace('\t', '').lower():
                print('\nOpenSong /test message received from ', message.author, ' on ', message.created_at)
                status_message = startup_validation.run_test_scripts()  # *************************************
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
                textFile = open(bulletin_path + filelist.DiscordMessageFilename, 'w', encoding='utf-8', errors='ignore')
                textFile.writelines(message)
                textFile.close()

                # --- parse the incoming Discord message
                status_message = utils.parsemessage()
                # --- check if a valid status message was received
                if status_message:
                    # --- update the current processing status
                    status_message = monitorfiles.filechecker()

                status_message = status_message + '\nOpenSong  {} command received'.format(message)
                print(status_message)
                await channel.send(status_message)


                return ()

            # --- check for the /newsong command -----
            elif '/addsong' in msg.replace(" ", '').replace('\t', '').lower() or '/new' in msg.replace(" ", '').replace(
                    '\t', '').lower():
                message_text = message.content.replace('-', ' ').replace('<', '').replace('>', '')

                try:
                    # --- split the line at the first space to retrieve the song name
                    command, songname = message_text.split(' ', 1)
                    if message.attachments:  # --- check for attachments

                        # -- save the attachement
                        await message.attachments[0].save(bulletin_path + filelist.NewSongTextFilename)
                        # --- call the addsong routine  ***********************************
                        status_message = maintainsong.addsong(songname)
                        # --- attempt to display the song which was just added
                        status_message = 'Use /search ' + songname + ' to display the song'
                        await message.channel.send(status_message)
                    else:
                        status_message = 'Missing file attachment with song lyrics!'
                        await message.channel.send(status_message)

                except ValueError:
                    status_message = 'Missing song name. Song name is required!'
                    await message.channel.send(status_message)

            # --- check for the /displaysong command -----
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
                    #set_date = str(getdatetime.nextSunday())  # --- set the default date of the next Sunday
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

            # --- check for the /help command -----
            elif '/help' in msg.replace(" ", '').replace('\t', '').lower():
                help_messages = ['The following commands are available ("/" is required):\n',
                                 '1. /status or /check\n',
                                 '2. /sync (forces sync from OpenSong to the gccpraise website\n',
                                 '3. /update (apply specific changes from a new post\n',
                                 '4. /addsong - <song name>\n',
                                 '5. /search <song name>\n',
                                 '6. /displayset <optional setDate in yyyy-mm-dd format>\n',
                                 '7. /help (to display this message)\n']
                # print('\nOpenSong Help command received from', message.author, ' on ', message.created_at)

                # --- post help message
                for x in help_messages:
                    await message.channel.send(x)
                return ()

            elif message.content.startswith('/hello'):
                await message.channel.send('Hello right back at you!')  # --- just for fun, reply to the same channel
                return

            # --- check for the /sync command (forces the rclone sync to the website -----
            elif '/sync' in msg.replace(" ", '').replace('\t', '').lower():
                # print('\nOpenSong Update Song message received from', message.author, ' on ', message.created_at)
                subprocess.Popen('/root/Dropbox/OpenSongV2/rclone-cron.sh')  # --- run the rclone sync process
                status_message = 'Discord Update Song <sync> processing completed'
                # print('\nCurrent Status=', status_message)

                # --- post Update Song process completed message
                await message.channel.send(status_message)

            elif msg.startswith('/'):
                channel = client.get_channel(opensong)
                reply_message = 'Unknown command received - no action taken'
                await message.channel.send(reply_message)
                message_author = str(message.author)
                reply_message = 'Message=', msg, ' received from:', message_author
                await message.channel.send(reply_message)
                reply_message = 'Use "/Help" for more information'
                await message.channel.send(reply_message)
                return

        return

    # --- Start the bot
    client.run(os.environ['DISCORD_TOKEN'])  # --- logon token retrieved from .env variable
    # --- End of Discord Bot

# ------------end of status checks


def main():
    # ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
    #--- Execute the main function
    read_discord()
    return ()

    # ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
    #
    if __name__ == "__main__":
        main()
#
# ======================================================================================
