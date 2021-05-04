# ---- function to perform basic test Discord Bot functionality
def run_test_scripts():
    import mydiscord
    import downloadbulletin
    import  monitorfiles
    import os
    import filelist

    #--- test functionality outside the Discord bot
    print('\nStart End-to-end Testing Script for Discord Bot processing\n')

    # --- Parse the incoming Discord message which is saved in a file
    print('\nTest Script #1 - mydiscord.parsemessages')
    status_message = mydiscord.parsemessage()
    print(status_message)


    # --- test the restore files process to be able to rerun the entire process
    print('\nTest Script #2 - mydiscord.restoreprocess')
    status_message = mydiscord.restoreprocess()
    print(status_message)

    if 'Waiting on Worship Schedule' in status_message:
        status_message = downloadbulletin.get_bulletin()    #--- download the latest bulletin file if one does not exit
        print('\nReturn from Download bulletin:\n', status_message)

        try:
            # --- rename the Old Worship Schedule file
            if os.path.isfile(filelist.OldWorshipScheduleFilename):
                os.replace(filelist.OldWorshipScheduleFilename, filelist.WorshipScheduleFilename)
            else:
                print("Worship Schedule file {} does not exist. Worship Schedule must be manually posted...".format(
                filelist.OldWorshipScheduleFilename))
        except:
            print("Old Worship Schedule file does not {} exists. Rename not performed...".format(
            filelist.OldWorshipScheduleFilename))


    if 'Waiting on Bulletin post' in status_message:
        status_message = downloadbulletin.get_bulletin()    #--- download the latest bulletin file if one does not exit
        print('\nReturn from Download bulletin:\n', status_message)

    # --- test the monitor files function to check the overall satus of processing
    print('\nTest Script #3 - monitorfiles.filechecker')
    status_message = monitorfiles.filechecker()
    print(status_message)

    # --- test the $displaysong functionality
    print('\nTest Script #4 - $displaysong\n')
    status_message = test_displaysong(message='$displaysong marvelous')
    print(status_message)

    # --- test the $displayset functionality
    print('\nTest Script #5 - $displayset\n')
    test_displayset(message='$displayset')

    #--- end testing script
    print('\nEnd-to_end Testing Script completed!')

# ---- end of testscript functionality 


def test_displaysong(message='$displaysong'):
    import maintainsong

 # --- Test the $displaysong functionality -----
    status_text = '\nStart {} command received'.format(message)
    print(status_text)
 
    if ' ' in message:
        # --- split the line at the first space to retrieve the song name
        command, song_name = message.split(' ',1)
        #print('\nSong name =', song_name)
        song_matches = {}
        # --- call the searchsong function
        song_matches = maintainsong.search_songs(song_name)

        if len(song_matches) == 0:
            status_message = '\nNo songs matching: {} found!)'.format(song_name)
            print(status_message)
        else:
            for song, url in song_matches.items():
                print('\nsong:', song, 'url:', url)
    else:
        status_message = '\nAt least a partial Song name is required for lookup\n'
        print(status_message)
# ---- end of test $displaysong functionality 

def test_displayset(message='$displayset'):
    import maintainsong
    import getdatetime

 # --- Test the $displaysong functionality -----
    status_text = '\nStart {} command received'.format(message)
    print(status_text)
    set_matches = {}
 
    if ' ' in message:
        # --- split the line at the first space to retrieve the song name
        command, set_date.split(' ',1)
        #print('\nSong name =', song_name)
        # --- call the searchsong function
        set_matches = maintainsong.displaySet(set_date)
    else:
        set_date = str(getdatetime.nextSunday())  # --- set the default date of the next Sunday
        set_matches = maintainsong.displaySet()  # --- call the DisplaySet function and use the default date ***********************

    if len(set_matches) == 0:
        status_message = '\nNo sets matching: {} found!)'.format(set_date)
        print(status_message)
    else:
        for myset in set_matches.items():
            print(myset)

    #print(status_message)
# ---- end of test $displaysong functionality 

def main():
    #--- =============================
    run_test_scripts()
    
    return()

# ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
#
if __name__ == "__main__":
    main()
#
# ======================================================================================
