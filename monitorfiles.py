# ------------ Watcher Script to monitor website for changes to a directory
# --- Also checks if all the prerequisite processing is complete (files created)
# --- https://veteransec.com/2020/05/08/python-script-to-monitor-website-changes/
# --- https://www.geeksforgeeks.org/python-script-to-monitor-website-changes/
import os
import readbulletin
import opensong
import downloadbulletin
import getdatetime  # --- get the current date / time
import filelist  # --- module to include standard list of all file names used in the process

import filelist  # --- definition of list of files and directories used in the proces


def filechecker():
    file_count = 0  # --- keep track of which files have been created
    status_message = ''

    bulletin_date = str(getdatetime.nextSunday())        #--- determine the bulletin date (next sunday relative to today)

    current_date_time = str(getdatetime.currentdatetime())
    status_message = 'Status check process started at:' + current_date_time + '\n for bulletin date: ' + bulletin_date + '\n'

    if os.environ['ENVIRON'] == 'PROD':
        setNameAttrib = bulletin_date + ' GCCEM Sunday Worship'
    else:
        setNameAttrib = os.environ['COMPUTERNAME'] + ' GCCEM Sunday Worship' 

    current_working_directory = os.getcwd()
    #print('\nMonitorFiles() Current Working Directory:', current_working_directory)

    if not 'sets' in current_working_directory:
        set_path='../sets'
        os.chdir(set_path)          #-- change to the sets directory

    if os.path.isfile(setNameAttrib):			#--- check if the set already exists
        status_message = '\nSet processing already completed for {}'.format(setNameAttrib)
        return(status_message)

    #--- switch back to the bulletin directory to continue processing
    current_working_directory = os.getcwd()
    if not 'bulletin' in current_working_directory:
        bulletin_path='../bulletin'
        os.chdir(bulletin_path)  # -- switch back to the default directory
        current_working_directory = os.getcwd()
        #print('\nMonitorFiles() Bulletin Working Directory:', current_working_directory)

    # --- check if sermon info file exists
    if not os.path.isfile(filelist.SermonInfoFilename):
        file_status = str("File {} does not exist....".format(filelist.SermonInfoFilename))
        status_message = status_message + file_status
        status_message = status_message + 'Waiting on Sermon Information message post!\n'
    else:
        file_count += 1  # --- increment the file watcher count
        # print('\nFileChecker - Assurance.txt file found:', filelist.AssuranceFilename)
        status_message = status_message + 'Sermon Information ready!\n'

    # --- check if assurance file exists
    if not os.path.isfile(filelist.AssuranceFilename):
        file_status = str("File {} does not exist....".format(filelist.AssuranceFilename))
        status_message = status_message + file_status
        status_message = status_message + 'Waiting on Assurance of Pardon message post!\n'
    else:
        file_count += 1  # --- increment the file watcher count
        # print('\nFileChecker - Assurance.txt file found:', filelist.AssuranceFilename)
        status_message = status_message + 'Assurance of Pardon ready!\n'

    # --- check if confession file exists
    if not os.path.isfile(filelist.ConfessionFilename):
        file_status = str("File {} does not exist....".format(filelist.ConfessionFilename))
        status_message = status_message + file_status
        status_message = status_message + 'Waiting on Confession of Sin message post!\n'
    else:
        file_count += 1  # --- increment the file watcher count
        # print('\nFileChecker - Confession.txt file found:', filelist.ConfessionFilename)
        status_message = status_message + 'Confession of Sin ready!\n'

    # --- check if worshipschedule file exists
    if not os.path.isfile(filelist.WorshipScheduleFilename):
        file_status = str( "File {} does not exist....".format(filelist.WorshipScheduleFilename))
        status_message = status_message + file_status
        status_message = status_message + 'Waiting on Worship Schedule post!\n'
    else:
        file_count += 1  # --- increment the file watcher count
        # print('\nFileChecker - WorshipSchedule.txt file found:', filelist.WorshipScheduleFilename)
        status_message = status_message + 'Worship Schedule ready!\n'

    # --- check if bulletin file exists
    # print('\nFilechecker - looking for text bulletin file:', filelist.TextBulletinFilename)
    if not os.path.isfile(filelist.TextBulletinFilename):  # --- if all prerequisites files exist, check for the bulletin file
        file_status = str( "File {} does not exist....".format(filelist.TextBulletinFilename))
        status_message = status_message + file_status
        status_message = status_message + 'Waiting on Bulletin post!\n'
    else:
        # --- begin the main process - all requirements met
        file_count += 1  # --- increment the file watcher count
        status_message = status_message + 'Bulletin ready!\n'

    # --- write the current status file
    textFile = open(filelist.CurrentStatusFilename, 'w', encoding='utf-8', errors='ignore')
    textFile.write(status_message)
    textFile.close()

    if file_count == 5:  # --- if all the prerequisite have been created check for a new bulletin
        status_message = status_message + 'All necessary files created.  OpenSong processing can proceed'
        #print(status_message)
        # --- start the build set process
        assemble_status_message = opensong.assembleset()  # --- all files exist, run the buildset process
        status_message = status_message + str(assemble_status_message)

    return discord.Embed(title='success', color = 0xe74c3c, description=status_message)


# --- function to read the key files, extract the date and very that the indidcated dates match
# --- https://www.blog.pythonlibrary.org/2018/05/09/determining-if-all-elements-in-a-list-are-the-same-in-python/
def comparefiledates():
    listofdates = []

    # --- get bulletin dates
    textFile = open(filelist.BulletinFilename, 'r', encoding='utf-8', errors='ignore')
    filedate = textFile.read()  # --- read the file into a string
    textFile.close()
    # --- parse the date and add to the list
    returned_date = getdatetime.parsedates(filedate)
    # print('\nCompare File Dates - returned date:', returned_date)
    listofdates.append(returned_date)

    # --- get Assurance of Pardon dates
    textFile = open(filelist.AssuranceFilename, 'r', encoding='utf-8', errors='ignore')
    filedate = textFile.read()  # --- read the file into a string
    textFile.close()
    # --- parse the date and add to the list
    filedate = filedate.split(",", 1)
    # print('\nAssurance of Pardon date=', filedate)
    returned_date = getdatetime.parsedates(filedate)
    # print('\nCompare File Dates - returned date:', returned_date)
    listofdates.append(returned_date)

    # --- get Confession of Sin dates
    textFile = open(filelist.ConfessionFilename, 'r', encoding='utf-8', errors='ignore')
    filedate = textFile.read()  # --- read the file into a string
    textFile.close()
    # --- parse the date and add to the list
    filedate = filedate.split(",", 1)
    # print('\nAssurance of Pardon date=', filedate)
    returned_date = getdatetime.parsedates(filedate)
    # print('\nCompare File Dates - returned date:', returned_date)
    listofdates.append(returned_date)

    # --- get Worship Schedule dates
    textFile = open(filelist.WorshipScheduleFilename, 'r', encoding='utf-8', errors='ignore')
    filedate = textFile.read()  # --- read the file into a string
    textFile.close()
    # --- parse the date and add to the list
    filedate = filedate.split(",", 1)
    # print('\nAssurance of Pardon date=', filedate)
    returned_date = getdatetime.parsedates(filedate)
    print('\nWorship Schedule Date:', returned_date)
    # print('\nCompare File Dates - returned date:', returned_date)
    listofdates.append(returned_date)

    print('\nListOfDates=', listofdates)

    if len(listofdates) < 1:
        print('\nAll dates match')
    # return True
    if len(listofdates) == listofdates.count(listofdates[0]):
        print('\nMonitorfiles.CompareFileDates - all dates match for:', listofdates[0])
    else:
        print('\nMonitorfiles.CompareFileDates - processing incomplete for:', listofdates[0])
        print('\nDates found: ', listofdates)

    return ()

# ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
def main():
    status_message = filechecker()
    print('\nReturn from monitor files:\n', status_message)


# ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
#
if __name__ == "__main__":
    main()
#
# ======================================================================================
