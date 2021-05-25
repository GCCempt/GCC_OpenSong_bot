# ---- function to perform basic test Discord Bot functionality
import utils
import readworshipschedule

set_path = 'sets/'
bulletin_path = 'bulletin/'


def run_test_scripts():
    import mydiscord
    import downloadbulletin
    import monitorfiles
    import os
    import filelist
    from monitorfiles import cleanup, set_cleanup

    # --- test functionality outside the Discord bot
    print('\nStart End-to-end Testing Script for Discord Bot processing\n')
    print('\nRuntime Environment=', os.environ['ENVIRON'])

    #--- cleanup any residual files before beginning processing
    #cleanup()       #--- call the cleanup routine to remove files and reset state for real processing
    #set_cleanup()     #--- clean up the OpenSong set file if running in DEV

    # --- Parse the incoming Discord message which is saved in a file
    print('\nTest Script #1 - parsemessages')
    status_message = str(utils.parsemessage())
    #print(status_message)

    if 'does not exist' in status_message:      #--- message.txt file does not exist
        status_message = build_message_file()   #--- create a dummy message file
        status_message = str(utils.parsemessage())
    
    print(status_message)

    # --- test the build worship schedule process
    print('\nTest Script #2 - build worship schedule')
    status_message = build_worship_schedule_file()

    readworshipschedule.readWS()  # read the worship schedule file extracted from discord and write the songs.txtfile

    print(status_message)

    print('\nTest Script #3 - Post the bulletin')
    status_message = downloadbulletin.get_bulletin()    #--- download the latest bulletin file if one does not exit
    print('\nReturn from Download bulletin:\n', status_message)

    # --- test the monitor files function to check the overall satus of processing
    print('\nTest Script #4 - monitorfiles.filechecker')
    status_message = monitorfiles.filechecker()
    print(status_message)

    # --- test the /displaysong functionality
    print('\nTest Script #5 - /displaysong\n')
    status_message = test_displaysong(message='/displaysong marvelous')
    print(status_message)

    # --- test the /displayset functionality
    print('\nTest Script #6 - /displayset\n')
    test_displayset(message='/displayset')

 # --- test the /status functionality
    print('\nTest Script #7 - /status\n')
    status_message = monitorfiles.statuscheck()
    print(status_message)

    #--- cleanup after yourself - remove files which were created for the validation process
    print('\nTest Script #8 - Cleanup')
    set_cleanup()
  
    #--- end testing script
    status_message = '\nEnd-to-end Testing Script completed!'
    print(status_message)
    return(status_message)

# ---- end of testscript functionality 


def test_displaysong(message='$display_song'):
    # --- Test the $display_song functionality -----
    status_text = '\nStart {} command received'.format(message)
    print(status_text)
 
    if ' ' in message:
        # --- split the line at the first space to retrieve the song name
        command, song_name = message.split(' ',1)
        #print('\nSong name =', url)
        song_matches = {}
        # --- call the searchsong function
        song_matches = utils.search_songs(song_name)

        if len(song_matches) == 0:
            status_message = '\nNo songs matching: {} found!)'.format(song_name)
            print(status_message)
        else:
            for song, url in song_matches.items():
                print('\nsong:', song, 'url:', url)
    else:
        status_message = '\nAt least a partial Song name is required for lookup\n'
        print(status_message)
# ---- end of test /displaysong functionality

def test_displayset(message='/displayset'):
    import maintainsong
    import getdatetime
    import os

 # --- Test the /displaysong functionality -----
    status_text = '\nStart {} command received'.format(message)
    print(status_text)
    set_matches = {}

    setNameAttrib = utils.generate_set_name()        #--- get the generated set name

    set_matches = maintainsong.displaySet(setNameAttrib)

    if len(set_matches) == 0:
        status_message = '\nNo sets matching: {} found!)'.format(setNameAttrib)
        print(status_message)
    else:
        for myset in set_matches.items():
            print(myset)

    #print(status_message)
# ---- end of test /displaysong functionality

def build_message_file():
    import filelist

    message_text = "Dear all, here is my sermon info for this Sunday, 1/1: \
    \nSample Message: The Gospel Mentality” (Galatians 3:1–14) \n \
    \nhere is the confession of sin to be put on screen, 1/1: \
    \nSample Confession: Almighty God, Father of our Lord Jesus Christ, \
        Maker of all things, Judge of all men; we acknowledge and bewail our manifold sins and wickedness, \
            which we, from time to time, most grievously have committed, by thought, word, and deed, \
                against Your Divine Majesty, provoking most justly Your wrath and indignation against us. \
    \nhere is the assurance of pardon to be put on screen, 1/1: \
    \nPsalm 103:11–13 \
    \nSample Assurance: For as high as the heavens are above the earth, \
        so great is his steadfast love toward those who fear him; \
            as far as the east is from the west, so far does he remove our transgressions from us. \
                As a father shows compassion to his children, so the LORD shows compassion to those who fear him."

 # --- write a dummy message.txt file -----
    textFile = open(bulletin_path + filelist.DiscordMessageFilename, 'w', encoding='utf-8', errors='ignore')
    textFile.write(message_text)
    textFile.close()

    status_message ='\nMessage text file created'

    return(status_message)
 # ---- end of build Message File functionality 

def build_worship_schedule_file():
    import filelist

    worship_text = "1/1 Worship Schedule \
    \nWorship Leader: Elder Eric \
    \nSpeaker: Pastor Arthur \
    \nHymn: Jesus Shall Reign (To Our King Be Highest Praise) - V1 V2 C V3 C V4 C C \
    \nPraise Team \
    \nElder Eric, Judy \
    \nBooth \
    \nComputer: Mr. Rogers \
    \nSound: Caleb \
    \nCamera: Daniel \
    \nSongs \
    \n* Still - V1 C V2 C C E \
    \n* Come Behold The Wondrous Mystery - V1 V2 V3 V4 E \
    \n* By Faith - V1 V2 C V3 V4 C V5 C C T"

    # --- write a dummy message.txt file -----
    textFile = open(bulletin_path + filelist.WorshipScheduleFilename, 'w', encoding='utf-8', errors='ignore')
    textFile.write(worship_text)
    textFile.close()
   
    status_message ='\nWorship Schedule text file created'

    return(status_message)
 # ---- end of build Worship Schedule functionality 

def build_sermon_info_file():
    import filelist

    sermon_info_text = " \
        @here Dear all, here is my sermon info for this Sunday, 1/1: \
        \nSample Message: The Gospel Mentality” (Galatians 3:1–14)"

    # --- write a dummy sermoninfo.txt file -----
    textFile = open(bulletin_path + filelist.SermonInfoFilename, 'w', encoding='utf-8', errors='ignore')
    textFile.write(sermon_info_text)
    textFile.close()
   
    status_message ='\nSermon Info text file created'

    return(status_message)
 # ---- end of build Worship Schedule functionality 

def main():
    #--- =============================
    status_message = run_test_scripts()

    print(status_message)
    return()

# ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
#
if __name__ == "__main__":
    main()
#
# ======================================================================================
