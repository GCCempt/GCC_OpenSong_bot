#-------- Read Discord Messages -last updated 03/02/2021 by Steve Rogers
#! python3
import discord
import os
import sys
from decouple import config
import monitorfiles
import opensong                     #--- my modulue to build the OpenSong set based on bulletin content and Discord postings
import filelist                 #--- definition of list of files and directories used in the proces
import getdatetime              #--- my module to get the current date / time
import subprocess               #--- for launching external shell commands
import downloadbulletin         #--- my module for downloading the bulletin
import stringsplit              #--- my module to split a string based on different criteria
import maintainsong               #--- module to add a new song to OpenSong
import testdiscord             #--- module for testing added Discord Bot functions
import pandas as pd             #Python data analysis library

#--- Discord channels: read messages from both, write responses to the opensong channel
#--- #pt_announcement channel.id = 681180782240464897
#--- #opensong channel.id = 813193976555241532
#--- #testing channel.id = 402275911619182592

client = discord.Client()       #--- create and instance of the Discord client toconnect to Discord

#------------ How to code a Discord Bot
#https://www.freecodecamp.org/news/create-a-discord-bot-with-python/

def read_discord(arg):

    print("\n !!!Hello world - OpenSong Discord Client starting at", getdatetime.currentdatetime())
    
    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))
       #--- post the startup message
        if 'testing' in arg:
            #channel = client.get_channel(402275911619182592)        #--- post to the #testing channel
            status_message = 'Discord Bot started in testing mode at', getdatetime.currentdatetime()
            #await channel.send(status_message)
            print(status_message)

        else:
            #channel = client.get_channel(813193976555241532)        #--- post to the #opensong channel
            status_message = 'Discord Bot started at', getdatetime.currentdatetime()
            #await channel.send(status_message)
            print(status_message)

            #--- display the latest status
            status_message = statuscheck()           #--- status message returned as a 'list' ***********
            #--- post help message
            #channel = client.get_channel(813193976555241532)
            for x in status_message:
                #await channel.send(x)
             print(x)

    @client.event
    async def on_message(message):
        if message.author == client.user:       #--- don't respond to messages from yourself 
            return()

        msg = message.content                           #--- retrieve the Discord message and process below

        if (message.channel.id == 402275911619182592):   #--- check for messages on the #testing channel
            message_env = 'test'        #--- set the message environment variable to 'test' for reply messages to the #testing channel
            test_message = '\nTest Discord Message ', message.content,  'received on channel: ', message.channel, ' from: ', message.author, ' on ', message.created_at
            print(test_message)
            await message.channel.send(test_message)        #--- reply on the same channel
            #return()

        elif (message.channel.id == 681180782240464897):   #--- accept messages posts on the #pt-announcment 
            print('\nDiscord Message received on channel:', message.channel, ' from ', message.author, ' on ', message.created_at)
            channel = client.get_channel(813193976555241532)                 #--- configure #opensong channel to receive reply messages

            #--- check the Discord message is for the Bulletin post -----
            if 'bulletinhasbeenposted' in msg.replace(" ", '').replace('\t', '').lower():
                status_message = 'Bulletin posted message received from ' + str(message.author) + ' on ' + str(message.created_at)
                #print(status_message)
                await channel.send(status_message)

                #--- download the new bulletin
                downloadbulletin.get_bulletin()         #--- Download the bulletin which was just posted  ************************

            else:
                #--- write the Message to a file for later processingn
                textFile = open(filelist.DiscordMessageFilename, 'w', encoding='utf-8',errors='ignore')
                textFile.writelines(msg)
                textFile.close()
  
                status_message = parsemessage()       #--- parse the incoming Discord message   ***********************************
                if status_message:                      #--- check if a valid status message was received
                    monitorfiles.filechecker()              #--- update the current processing status
                    status_message = statuscheck()           #--- Post the current status on the opensong channel
                    for x in status_message:
                        await channel.send(x)
                elif (message.channel.id == 681180782240464897): #--- unrecognized message received on the #pt-announcment channel
                    reply_messages =['Unrecognized message "', message.content, '" received from', message.author, ' on ', message.created_at,
	                'The following message are accepted:',
                    '1. sermon info for <date>',
                    '2. confession of sin for <date>',
                    '3. assurance of pardon for <date>',
                    '4. worship schedule for <date>',
		            'Each message must be followed by the message content']

                    #--- post reply message to the opensong channel
                    for x in reply_messages:
                        await channel.send(x)
                else:
                    pass

        elif (message.channel.id == 813193976555241532):     #--only check for $commands on the #opensong channel
            #--- check for the $status command -----
            if '$status' in msg.replace(" ", '').replace('\t', '').lower() or '$check' in msg.replace(" ", '').replace('\t', '').lower():
                print('\nDiscord Check Status message received from ', message.author, ' on ', message.created_at)
                status_message = statuscheck()           #---read the current status message returned as a 'list'
            
                #--- post status message
                for x in status_message:
                    await message.channel.send(x)
                return()

            #--- check for the $cleanup command used when processing did not complete successfully -----
            elif '$cleanup' in msg.replace(" ", '').replace('\t', '').lower() or '$check' in msg.replace(" ", '').replace('\t', '').lower():
                print('\nDiscord Cleanup message received from ', message.author, ' on ', message.created_at)
                opensong.cleanup()          #---cleanup residual files ******************************
                return()

            #--- check for the $restore command message -----
            elif '$restore' in msg.replace(" ", '').replace('\t', '').lower():
                #print('\nOpenSong restore process message received from ', message.author, ' on ', message.created_at)
                restoreprocess()            #--- recover files to rerun the process *************************
                status_message = 'Discord restore processing completed'
                print('\nCurrent Status=', status_message)

                #--- post restore process completed message
                #await message.channel.send(status_message)
                status_message = statuscheck()           #--- status message returned as a 'list'
                #--- post status message
                for x in status_message:
                    #await message.channel.send(x)
                    print(x)
                return()

            #--- check for the $update command -----
            elif '$update' in msg.replace(" ", '').replace('\t', '').lower():
                print('\nOpenSong update message received from ', message.author, ' on ', message.created_at)
                updateprocess()             # *************************************
                status_message = 'Discord Update processing completed'
                #print('\nCurrent Status=', status_message)

                #--- post rerun process completed message
                await message.channel.send(status_message)
                status_message = statuscheck()           #--- status message returned as a 'list'
            
                #--- post status message
                for x in status_message:
                    await message.channel.send(x)
                return()

            #--- check for the $rerun command -----
            elif '$rerun' in msg.replace(" ", '').replace('\t', '').lower():
                print('\nOpenSong $rerun message received from ', message.author, ' on ', message.created_at)
                monitorfiles.filechecker()            # *************************************
                status_message = '$rerun processing completed!'

                return()

                #------------check for $repost command Used to fetch "old" message identified by message link and save it to a file  
                #--- https://levelup.gitconnected.com/how-to-gather-message-data-using-a-discord-bot-from-scratch-with-python-2fe239da3bcd (get historical messages)
            elif '$repost' in msg.lower():

                #channel = client.get_channel(681180782240464897)   #--- get the channelId of the #pt-announcment channel 
                #await channel.send('hello')

                cmd = message.content.split()[0]        #--- split the command and parameters
                if len(message.content.split()) > 1:      #--- check if a parameter was passed
                    parameter = message.content.split()[1:] #--- get the message link as the parameter on the command
                    parameter = parameter[0].strip("']")
                    #print('\nparameter=', parameter)

                    items = str(parameter).split('/')      #--- break the https message link into a list of items;
                    #for i in range(0, len(items)):
                    #    print(i, items[i])

                    server_id = int(items[4])
                    channel_id = int(items[5])         #--- retrive the channelID from the parsed message link
                    message_id = int(items[6])        #--- retrieve the messageID from the parsed message link

                    server = client.get_guild(server_id)
                    channel = server.get_channel(channel_id)
                    message_post = await channel.fetch_message(message_id)
                    message = message_post.content

                else:
                    status_message ='\nMissing Message link; message link is required'
                    await message.channel.send(status_message)
                    print(status_message)
                    return()
                
                #print('\nMessage retrived', message.content)

                #--- write the Message to a file for later processingn
                textFile = open(filelist.DiscordMessageFilename, 'w', encoding='utf-8',errors='ignore')
                textFile.writelines(message)
                textFile.close()
  
                status_message = parsemessage()       #--- parse the incoming Discord message   ***********************************
                if status_message:                      #--- check if a valid status message was received
                    monitorfiles.filechecker()              #--- update the current processing status
                    status_message = statuscheck()           #--- Post the current status on the opensong channel
                    for x in status_message:
                        await channel.send(x)

                status_text = '\nOpenSong  {} command received'. format(message)
                print(status_text)
                return()

            #--- check for the $newsong command -----
            elif '$add' in msg.replace(" ", '').replace('\t', '').lower() or '$new' in msg.replace(" ", '').replace('\t', '').lower():
                #print('\nOpenSong New Song message received', message.content, ' from ', message.author, ' on ', message.created_at)
                message_text = message.content.replace('-', ' ').replace('<', '').replace('>', '')
            
                try:
                    command, songname = message_text.split(' ', 1)          #--- split the line at the first space to retrieve the song name
                    if message.attachments:         #--- check for attachments
                        await message.attachments[0].save(filelist.NewSongTextFilename)         #-- save the attachement
                        status_message = maintainsong.addsong(songname)     #--- call the addsong routine  ***********************************
                        #--- attempt to display the song which was just added
                        status_message = 'Use $search ' + songname + ' to display the song'
                        await message.channel.send(status_message)
                    else:
                        status_message = 'Missing file attachment with song lyrics!'
                        await message.channel.send(status_message)

                except ValueError:
                    status_message = 'Missing song name. Song name is required!'
                    await message.channel.send(status_message)

            #--- check for the $displaysong command -----
            elif '$searchsong' in msg.replace(" ", '').replace('\t', '').lower():
                status_text = '\nOpenSong  {} command received'. format(message.content)
                print(status_text)
                message_text = message.content
                if ' ' in message_text:
                    command, song_name = message.content.split(' ', 1)          #--- split the line at the first space to retrieve the song name
                    print('\nSong name =', song_name)
                    song_matches = {}
                    song_matches = maintainsong.search_songs(song_name)          #--- call the searchsong function   ***********************
                    if len(song_matches) == 0:
                        status_message = '\nNo songs matching: {} found!)'. format(song_name)
                        #print(status_message)
                        await message.channel.send(status_message)
                    else:
                        #print('\nSong {} Found)'. format(url))
                        #--- post returned URL
                        for song, url in song_matches.items():
                            embed = discord.Embed()
                            embed.description = '[' + song + '](' + url +')'
                            status_message = embed.description
                            #--- post embed message
                            await message.channel.send(embed=embed)

            elif '$displayset' in msg.replace(" ", '').replace('\t', '').lower():
                returned_elements = maintainsong.bs4buildSetSummary()
                print(returned_elements)


                status_text = '\nOpenSong  {} command received'. format(message.content)
                print(status_text)
                set_matches = {}
                message_text = message.content

                if ' ' in message_text:
                    command, set_date = message.content.split(' ', 1)          #--- split the line at the first space to retrieve the song name
                    print('\nInput Set Date =', set_date)

                    set_matches = maintainsong.displaySet(set_date)          #--- call the DisplaySet function  with the specified date ***********************
                else:
                    set_date = str(getdatetime.nextSunday())                  #--- set the default date of the next Sunday
                    set_matches = maintainsong.displaySet()          #--- call the DisplaySet function and use the default date ***********************

                if len(set_matches) == 0:
                    status_message = '\nNo sets matching: {} found!'. format(set_date)
                    #print(status_message)
                    await message.channel.send(status_message)
                else:
                    #print('\nSong {} Found)'. format(url))
                    #--- post returned URL
                    for myset, url in set_matches.items():
                        embed = discord.Embed()
                        embed.description = '[' + myset + '](' + url +')'
                        status_message = embed.description
                        #--- post embed message
                        await message.channel.send(embed=embed)
                
                if len(set_matches) == 1:
                    returned_elements = maintainsong.bs4buildSetSummary(myset)
                    status_message = '\n'.join(returned_elements)  #--- convert list to string
                    print(status_message)
                    await message.channel.send(status_message)

            #--- check for the $help command -----
            elif '$help' in msg.replace(" ", '').replace('\t', '').lower():
                help_messages =['The following commands are available ("$" is required):\n',
                '1. $status or $check\n',
                '2. $sync (forces sync from OpenSong to the gccpraise website\n',
                '3. $update (apply specific changes from a new post\n',
                '4. $addsong - <song name>\n',
                '5. $search <song name>\n',
                '6. $displayset <optional setDate in yyyy-mm-dd format>\n',
                '7. $help (to display this message)\n']
                #print('\nOpenSong Help command received from', message.author, ' on ', message.created_at)

                #--- post help message
                for x in help_messages:
                    await message.channel.send(x)
                return()

            elif message.content.startswith('$hello'):
                await message.channel.send('Hello right back at you!')        #--- just for fun, reply to the same channel
                return

        #--- check for the $sync command (forces the rclone sync to the website -----
            elif '$sync' in msg.replace(" ", '').replace('\t', '').lower():
                #print('\nOpenSong Update Song message received from', message.author, ' on ', message.created_at)
                subprocess.Popen('/root/Dropbox/OpenSongV2/rclone-cron.sh')                  #--- run the rclone sync process
                status_message = 'Discord Update Song <sync> processing completed'
                #print('\nCurrent Status=', status_message)

            #--- post Update Song process completed message
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
    #--- Start the bot
    client.run(config('TOKEN'))                 #--- logon token retrieved from .env variable
    #--- End of Discord Bot

#--- Parse the incoming Discord message   
def parsemessage():
    #--- Read the Discord message file
    textFile = open(filelist.DiscordMessageFilename, 'r', encoding='utf-8',errors='ignore')
    Lines = textFile.readlines()              #--- read the first line from the file
    textFile.close()

    status_message = []
    valid_message = ''

    for i in range(0, len(Lines)-1):
    #--- check for worship schedule message
        if 'worshipschedule' in Lines[i].replace(" ", '').replace('\t', '').lower():
            valid_message = 'true'
            worshipschedule =[]
            status_message.append('Worship Schedule message received')
            for j in range(i, len(Lines)):
                line = Lines[j]
                worshipschedule.append(line)
                j +=1
            #--- write the worship schedule file
            textFile = open(filelist.WorshipScheduleFilename, 'w', encoding='utf-8',errors='ignore')
            textFile.writelines(worshipschedule)
            textFile.close()
            i = j           #--- reset the line pointer in the file

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
                    if '@here' in Lines[j+1]:
                        break
                j +=1

            #print('\nWorship Schedule file name is:', filelist.WorshipScheduleFilename)
            #--- write the Sermon Info file
            textFile = open(filelist.SermonInfoFilename, 'w', encoding='utf-8',errors='ignore')
            textFile.writelines(sermoninfo)
            textFile.close()
            i = j           #--- reset the line pointer in the file

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
                    if '@here' in Lines[j+1]:
                        break
                j +=1

            #--- write the Confession of Sin file
            textFile = open(filelist.ConfessionFilename, 'w', encoding='utf-8',errors='ignore')
            textFile.writelines(confessioninfo)
            textFile.close()
            i = j           #--- reset the line pointer in the file

        elif 'assuranceofpardon' in Lines[i].replace(" ", '').replace('\t', '').lower():
            valid_message = 'true'
            assuranceinfo = []
            status_message.append('Assurance of Pardon message received')

            for j in range(i, len(Lines)):
                line = Lines[j]
                #print('\nAof line: j=', j, ' line=', line, ' len=', len(Lines))
                assuranceinfo.append(line)
                if j + 1 == len(Lines):
                    break
                else:
                    if '@here' in Lines[j+1]:
                        break
                j +=1

            #--- write the Assurance of Pardon
            textFile = open(filelist.AssuranceFilename, 'w', encoding='utf-8',errors='ignore')
            textFile.writelines(assuranceinfo)
            textFile.close()
            i = j           #--- reset the line pointer in the file

        i +=1
    if valid_message:
        return(status_message)      #--- if a valid message was posted, return status message as a list
 #------------end of status checks  

#------------Start -  Re-run the OpenSong proces  
def restoreprocess():
    #--- rename the previous processing files to prepare for re-running the process
    #--- Check if there is a new file first
	#--- rename the Old Assurance of Faith file
    #--- $restore command (execute the process build the set from the previous content) \n',
    print("\n !!!Warning -- this will overwrite any currently posted files!!! OpenSong restore processing starting at", getdatetime.currentdatetime())

	#--- rename the Old Assurance of Pardon of Sin file
    if os.path.isfile(filelist.OldAssuranceFilename):
        os.replace(filelist.OldAssuranceFilename, filelist.AssuranceFilename)
    else:
        print("Assurance of Pardon file {} does not exist. Assurance of Pardon must be manually posted...".format(filelist.OldAssuranceFilename))

	#--- rename the Old Confession of Sin file
    if os.path.isfile(filelist.ConfessionFilename):
        os.replace(filelist.OldConfessionFilename, filelist.ConfessionFilename)
    else:
        print("Confession of Sin file {} does not exist. Confession of Sin must be manually posted...".format(filelist.OldConfessionFilename))

	#--- rename the Old Worship Schedule file
    if os.path.isfile(filelist.WorshipScheduleFilename):
        os.replace(filelist.OldWorshipScheduleFilename, filelist.WorshipScheduleFilename)
    else:
        print("Worship Schedule file {} does not exist. Worship Schedule must be manually posted...".format(filelist.OldWorshipScheduleFilename))

	#--- rename the Old text Bulletin File
    if os.path.isfile(filelist.TextBulletinFilename):
        os.replace(filelist.OldTextBulletinFilename , filelist.TextBulletinFilename)
    else:
        print("Bulletin file {} does not exist. Bulletin posted message must be manually posted...".format(filelist.OldTextBulletinFilename))
	
    #--- rerun the main process
    monitorfiles.filechecker()

    return()
#--- End of rerun processing

#------------Start -  Re-run the OpenSong proces  
def updateprocess():
    #--- Use the '$update' command to modify the content of  previous post for this week's processing
    #--- Check if there is a new file first; if there is, use it, otherwise use the archive file
    print("\n !!!OpenSong update processing starting at", getdatetime.currentdatetime())

    #--- read the bulletin date file
    textFile = open(filelist.BulletinDateFilename, 'r', encoding='utf-8',errors='ignore')
    bulletin_date = textFile.read()              #--- read the first line from the file
    textFile.close()

    #--- get current date
    current_date = getdatetime.currentdate()             #--- get today's date
    #--- parse the date from the bulletin date file
    returned_date = getdatetime.parsedates(bulletin_date)

    #--- compare dates
    if current_date > returned_date:        #--- Bulletin has already been processed
        print('\nCurrent Date ', current_date, ' is later than Bulletin date=', returned_date)
        monitorfiles.filechecker()      #--- continue with normal processing
        return()
    else:
        print('\nBulletin Date ', bulletin_date, ' is later than Current Date=', current_date)

    if os.path.isfile(filelist.AssuranceFilename):          #--- new / updated file exists
        pass
    else:
        if os.path.isfile(filelist.OldAssuranceFilename):   #--- archive file exists and will be renamed to current
            os.replace(filelist.OldAssuranceFilename, filelist.AssuranceFilename)
        else:
            print("Assurance of Pardon file {} does not exist. Assurance of Faith must be posted...".format(filelist.OldAssuranceFilename))

	#--- check the Confession of Sin file
    if os.path.isfile(filelist.ConfessionFilename):
        pass
    else:
        if os.path.isfile(filelist.OldConfessionFilename):
            os.replace(filelist.OldConfessionFilename, filelist.ConfessionFilename)
        else:
           print("Confession of Sin file {} does not exist. Confession of Sin must be posted...".format(filelist.OldConfessionFilename))

	#--- Check the Worship Schedule file
    if os.path.isfile(filelist.WorshipScheduleFilename):
        pass
    else:
        if os.path.isfile(filelist.OldWorshipScheduleFilename):
            os.replace(filelist.OldWorshipScheduleFilename, filelist.WorshipScheduleFilename)
        else:
            print("Worship Schedule file {} does not exist. Worship Schedule must be posted...".format(filelist.OldWorshipScheduleFilename))

	#--- Check for the text Bulletin File
    if os.path.isfile(filelist.TextBulletinFilename):
        pass
    else:
        if os.path.isfile(filelist.OldTextBulletinFilename):
            os.replace(filelist.OldTextBulletinFilename , filelist.TextBulletinFilename )
        else:
            print("Bulletin file {} does not exist. New Bulletin text file must be posted...".format(filelist.OldTextBulletinFilename))

	#--- rerun the main process
    monitorfiles.filechecker()

    return()
#--- End of rerun processing


#------------on Bot start run the statuscheck process to check for system state to determine if processing can run  
def statuscheck():
    #--- Check the current directory location
    wk_dir = os.getcwd()
    print('\nStatus check - current working directory: ', wk_dir)

    if 'Sets' in wk_dir:
        os.chdir(filelist.bulletinpath)   #-- change to the Bulletin directory
        print('\nStatus Check - changed working directory: ', os.getcwd())
    
    #--- CHECK THE STATUS FILE FOR PROCESS SUCCESSFUL COMPLETION OF ALL PROCESSING
    if not os.path.isfile(filelist.CurrentStatusFilename):
        print("File path {} does not exist. Processing still pending...".format(filelist.StatusFile))
        status_message = 'Processing still pending....'
    else:
        textFile = open(filelist.CurrentStatusFilename, 'r', encoding='utf-8',errors='ignore')
        status_message = textFile.readlines()              #--- read the first line from the file
        textFile.close()

    return(status_message)      #--- return status message as a list
#------------end of status checks  
