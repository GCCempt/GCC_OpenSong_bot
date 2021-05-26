import filelist  # --- definition of list of files and directories used in the proces
from utils import read_ahead, write_message_file

# --- extract the announcement text from the bulletin.txt file, write to announcements.txt file  ------------------
def extract_announcement():
    bulletin_path = 'bulletin/'
    status_message =[]
    announcements = []
    announcement_text = ''

    try:
        # --- Read the bulletin text extracted from the pdf bulletin
        textFile = open(bulletin_path + filelist.TextBulletinFilename, 'r', encoding='utf-8', errors='ignore')
        Lines = textFile.readlines()  # --- read the file into a list
        #line = textFile.read()  # --- read the file into a list
        textFile.close()
    except:
        file_status = "Bulletin Text file {} does not exist........".format(bulletin_path + filelist.TextBulletinFilename)
        status_message.append(file_status)
        return (status_message)

    #--- process the file to extract the announcements
    items = read_ahead(Lines)
    item = items.__next__()    #-- get the first line

    while(item):
        next_line = items.__next__()

        if  'announcements' in item.replace(" ", '').replace('\t', '').lower():
            if 'doxology' in  next_line.replace(" ", '').replace('\t', '').lower():
                item = next_line    #-- get the next item
            else:
                status_message.append('\nAnnouncements received')
  
                item = next_line        #--- skip the first announcement line       
            
                while(item):
                    announcements.append(item)
                    announcement_text = announcement_text + item
                    next_line = items.__next__()
                    item = next_line    #-- get the next item

                    if '–––––––––––' in next_line or next_line == None:
                        status_message.append('\end of announcements')
                        final_text = parse_announcement(announcement_text)

                        write_message_file(final_text, filelist.AnnouncementFileName)

                        return(status_message)
                
        else:
            item = next_line    #-- get the next item
    return(status_message)

#--- end routine to extract announcement text

# --- parse the extracted announcement text from the bulletin.txt file, write to announcements.txt file  ------------------
def parse_announcement(announcement_text):
    import re
    from stringsplit import split_on_number

    announcements = []

    #split on number followed by period
    announcement_text = announcement_text.replace('\n', '')

    announcement_text = re.sub('(\s\d+)\.\s', convert_period_to_space, announcement_text)

    announcements = split_on_number(announcement_text)

    for my_announcement in announcements:
        hold_announcement = str(my_announcement)
        new_announcement = hold_announcement.lstrip(' ')
        print(new_announcement)

    status_message = 'split complete'
#--- end parse bulletin

# --- convert the announcement number followed by period to number followed by space ------------------
def convert_period_to_space(match_text):
    converted_text = match_text.group().replace('.', ' ')

    return(converted_text)

# --- end convert the announcement number

#--- routine to unit test independent functions
def main():
    #import utils
    #import readworshipschedule

    print('\nMy Test Routine - Start Test!\n')
    status_message = extract_announcement()
    print(status_message)

    return()


    # ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
    #
if __name__ == "__main__":
    main()
# ======================================================================================