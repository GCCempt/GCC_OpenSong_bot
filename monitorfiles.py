# ------------ Watcher Script to monitor website for changes to a directory
# --- Also checks if all the prerequisite processing is complete (files created)
# --- https://veteransec.com/2020/05/08/python-script-to-monitor-website-changes/
# --- https://www.geeksforgeeks.org/python-script-to-monitor-website-changes/
import logging
import os

import filelist  # --- definition of list of files and directories used in the proces
import getdatetime  # --- get the current date / time
import opensong
from utils import generate_set_name

set_path = 'sets/'
bulletin_path = 'bulletin/'


def filechecker():
    file_count = 0  # --- keep track of which files have been created
    status_message = ''

    # --- check if sermon info file exists
    if not os.path.isfile(bulletin_path + filelist.SermonInfoFilename):
        file_status = str("File {} does not exist....".format(bulletin_path + filelist.SermonInfoFilename))
        # status_message = status_message + file_status
        status_message = status_message + 'Sermon Information:' + '\u274C' + '\n'
    else:
        file_count += 1  # --- increment the file watcher count
        # print('\nFileChecker - Assurance.txt file found:', filelist.AssuranceFilename)
        status_message = status_message + 'Sermon Information:' + '\u2705' + '\n'

    # --- check if assurance file exists
    if not os.path.isfile(bulletin_path + filelist.AssuranceFilename):
        file_status = str("File {} does not exist....".format(bulletin_path + filelist.AssuranceFilename))
        # status_message = status_message + file_status
        status_message = status_message + 'Assurance of Pardon:' + '\u274C' + '\n'
    else:
        file_count += 1  # --- increment the file watcher count
        # print('\nFileChecker - Assurance.txt file found:', filelist.AssuranceFilename)
        status_message = status_message + 'Assurance of Pardon: ' + '\u2705' + '\n'

    # --- check if confession file exists
    if not os.path.isfile(bulletin_path + filelist.ConfessionFilename):
        file_status = str("File {} does not exist....".format(bulletin_path + filelist.ConfessionFilename))
        # status_message = status_message + file_status
        status_message = status_message + 'Confession of Sin: ' + '\u274C' + '\n'
    else:
        file_count += 1  # --- increment the file watcher count
        # print('\nFileChecker - Confession.txt file found:', filelist.ConfessionFilename)
        status_message = status_message + 'Confession of Sin: ' + '\u2705' + '\n'

    # --- check if worshipschedule file exists
    if not os.path.isfile(bulletin_path + filelist.WorshipScheduleFilename):
        file_status = str("File {} does not exist....".format(bulletin_path + filelist.WorshipScheduleFilename))
        # status_message = status_message + file_status
        status_message = status_message + 'Worship Schedule: ' + '\u274C' + '\n'
    else:
        file_count += 1  # --- increment the file watcher count
        # print('\nFileChecker - WorshipSchedule.txt file found:', filelist.WorshipScheduleFilename)
        status_message = status_message + 'Worship Schedule: ' + '\u2705' + '\n'

    # --- check if bulletin file exists
    # print('\nFilechecker - looking for text bulletin file:', filelist.TextBulletinFilename)
    if not os.path.isfile(
            bulletin_path + filelist.TextBulletinFilename):  # --- if all prerequisites files exist, check for the bulletin file
        file_status = str("File {} does not exist....".format(bulletin_path + filelist.TextBulletinFilename))
        # status_message = status_message + file_status
        status_message = status_message + 'Bulletin: ' + '\u274C' + '\n'
    else:
        # --- begin the main process - all requirements met
        file_count += 1  # --- increment the file watcher count
        status_message = status_message + 'Bulletin: ' + '\u2705' + '\n'

    # --- write the current status file
    textFile = open(bulletin_path + filelist.CurrentStatusFilename, 'w', encoding='utf-8', errors='ignore')
    textFile.write(status_message)
    textFile.close()

    if file_count == 5:  # --- if all the prerequisite have been created check for a new bulletin
        status_message = status_message + 'All necessary files created.  OpenSong processing can proceed'
        # print(status_message)
        # --- start the build set process
        assemble_status_message = opensong.assembleset()  # --- all files exist, run the buildset process
        status_message = status_message + str(assemble_status_message)

    return status_message


# --- function to read the key files, extract the date and very that the indidcated dates match
# --- https://www.blog.pythonlibrary.org/2018/05/09/determining-if-all-elements-in-a-list-are-the-same-in-python/
def comparefiledates():
    listofdates = []

    # --- get bulletin dates
    textFile = open(bulletin_path + filelist.BulletinFilename, 'r', encoding='utf-8', errors='ignore')
    filedate = textFile.read()  # --- read the file into a string
    textFile.close()
    # --- parse the date and add to the list
    returned_date = getdatetime.parsedates(filedate)
    # print('\nCompare File Dates - returned date:', returned_date)
    listofdates.append(returned_date)

    # --- get Assurance of Pardon dates
    textFile = open(bulletin_path + filelist.AssuranceFilename, 'r', encoding='utf-8', errors='ignore')
    filedate = textFile.read()  # --- read the file into a string
    textFile.close()
    # --- parse the date and add to the list
    filedate = filedate.split(",", 1)
    # print('\nAssurance of Pardon date=', filedate)
    returned_date = getdatetime.parsedates(filedate)
    # print('\nCompare File Dates - returned date:', returned_date)
    listofdates.append(returned_date)

    # --- get Confession of Sin dates
    textFile = open(bulletin_path + filelist.ConfessionFilename, 'r', encoding='utf-8', errors='ignore')
    filedate = textFile.read()  # --- read the file into a string
    textFile.close()
    # --- parse the date and add to the list
    filedate = filedate.split(",", 1)
    # print('\nAssurance of Pardon date=', filedate)
    returned_date = getdatetime.parsedates(filedate)
    # print('\nCompare File Dates - returned date:', returned_date)
    listofdates.append(returned_date)

    # --- get Worship Schedule dates
    textFile = open(bulletin_path + filelist.WorshipScheduleFilename, 'r', encoding='utf-8', errors='ignore')
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


# --- function to respond to the '/status' discord post command
def statuscheck():
    file_count = 0  # --- keep track of which files have been created
    status_message = ''

    # --- determine which date to use to check the bulletin status
    current_day = getdatetime.getDayOfWeek()
    if current_day == 'Sunday':  # --- if today is Sunday, use today's date
        bulletin_date = str(getdatetime.currentdatetime('%Y-%m-%d'))
    else:
        bulletin_date = str(getdatetime.nextSunday())  # --- use the upcoming Sunday

    current_date_time = str(getdatetime.currentdatetime())

    setNameAttrib = generate_set_name()

    status_message = 'Status check process started at:' + current_date_time + '\n for: ' + setNameAttrib + '\n'

    file_name = set_path + setNameAttrib
    if os.path.exists(file_name):
        status_message = status_message + '\nSet processing completed for {}'.format(setNameAttrib)
        return (status_message)
    else:
        new_status_message = filechecker()
        status_message = status_message + new_status_message
        return (status_message)


# --- end for statscheck()

# ------------Start -  cleanup process i.e. rename / delete files
def cleanup():
    import os.path

    file_list = []
    bulletin_path = 'bulletin/'
    set_path = 'sets/'

    status_message = '\n**File Clean up processing started!\n**'
    print(status_message)

    file_name = bulletin_path + filelist.SongsFileName
    file_list.append(file_name)

    file_name = bulletin_path + filelist.PDFBulletinFilename
    file_list.append(file_name)

    file_name = bulletin_path + filelist.TextBulletinFilename
    file_list.append(file_name)

    file_name = bulletin_path + filelist.WorshipScheduleFilename
    file_list.append(file_name)

    file_name = bulletin_path + filelist.AssuranceFilename
    file_list.append(file_name)

    file_name = bulletin_path + filelist.ConfessionFilename
    file_list.append(file_name)

    file_name = bulletin_path + filelist.SermonInfoFilename
    file_list.append(file_name)

    file_name = bulletin_path + filelist.CurrentStatusFilename
    file_list.append(file_name)

    file_name = bulletin_path + filelist.DiscordMessageFilename
    file_list.append(file_name)

    file_name = bulletin_path + filelist.BulletinDateFilename
    file_list.append(file_name)

    file_name = bulletin_path + filelist.SetFilename
    file_list.append(file_name)

    file_name = bulletin_path + filelist.AffirmationFileName
    file_list.append(file_name)

    file_name = bulletin_path + filelist.AnnouncementFileName
    file_list.append(file_name)

    file_name = bulletin_path + filelist.HTMLBulletinFilename
    file_list.append(file_name)

    file_name = bulletin_path + filelist.BulletinSermonFilename
    file_list.append(file_name)

    file_name = bulletin_path + filelist.CallToWorshipFileName
    file_list.append(file_name)

    file_name = bulletin_path + filelist.TextPDFBulletinFilename
    file_list.append(file_name)

    file_name = bulletin_path + filelist.ScriptureFileName
    file_list.append(file_name)

    file_name = bulletin_path + filelist.HTMLSermonScriptureFilename
    file_list.append(file_name)

    for myfile in file_list:
        try:
            os.remove(myfile)
        except OSError as e:
            logging.warning(e)
            status_message = status_message + '\nUnable to remove file {}..'.format(myfile)

    # --- update the current status
    # status_message = monitorfiles.filechecker()  # --- update the status file
    status_message = status_message + '\n**File Cleanup completed**'

    print(status_message)

    return status_message


# ------------End  -  cleanup process

# ------------Start -  cleanup process i.e. rename / delete files
def set_cleanup():
    from utils import generate_set_name

    # --- clean up the OpenSong set
    status_message = '\nSet Cleanup process started'
    # print(status_message)
    
    setNameAttrib = generate_set_name()
    file_name = set_path + setNameAttrib

    if os.path.exists(file_name):
        try:
            os.remove(file_name)
            status_message = status_message + '\nSet removed {}'.fornat(file_name)
        except OSError as e:
            logging.warning(e)
            status_message = status_message + '\nUnable to remove file {}..'.format(file_name)

    # --- clean up the OpenSong processing files
    cleanup_status = cleanup()
    status_message = status_message + cleanup_status

    print('\nFile Cleanup Processing completed!')

    return (status_message)


# ------------End  -  set_cleanup process


# ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
def main():
    status_message = filechecker()
    print('\nFile status:\n', status_message)


# ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
#
if __name__ == "__main__":
    main()
#
# ======================================================================================
