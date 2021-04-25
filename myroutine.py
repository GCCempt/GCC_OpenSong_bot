import sys
import readworshipschedule
import passagelookup  # --- modulue to do API lookup for ESV passage from Crossway
import opensong
import stringsplit
#import mydiscord
import monitorfiles
from datetime import datetime, timedelta
import maintainsong


def printBoard():
    rows, cols = 5, 5
    board = [['.' for i in range(cols)] for j in range(rows)]
    print('\nOriginal board=', board)

    board[3][3] = 'x'
    print('\nModified board=', board)

    for i in range(cols):
        for j in range(rows):
            print(board[i],[j])

    #        print(board[i:j])
     #   print(count, ',', j)

    #printBoard("."*60)
#--- end printBoard

# --- Covert string to standard date
def convertdates():
    from dateutil.parser import parse
    import stringsplit

    converted_date = stringsplit.split_on_number('Sunday, March 14, 2021  •  11:15 am ')
    print('Converted date:', converted_date)
    # dt = parse(converted_date)
    # print(dt.date())

    date_array = [
        '2018-06-29 08:15:27.243860',
        'Jun 28 2018 7:40AM',
        'Jun 28 2018 at 7:40AM',
        'September 18, 2017, 22:19:55',
        'Sun, 05/12/1999, 12:30PM',
        'Mon, 21 March, 2015',
        '2018-03-12T10:12:45Z',
        '2018-06-29 17:08:00.586525+00:00',
        '2018-06-29 17:08:00.586525+05:00',
        'Tuesday , 6th September, 2017 at 4:30pm',
        'Sunday, March 14, 2021'
    ]

    for date in date_array:
        print('Parsing dates: ' + date)
        dt = parse(date)
        print(dt.date())
        # print(dt.time())
        # print(dt.tzinfo)
        print('\n')

    return ()


# --- End Get the current date / time

# --- https://pymupdf.readthedocs.io/en/latest/tutorial.html
def readbulletin():
    import fitz
    import filelist

    with fitz.open('EM_Bulletin_v01.pdf') as doc:
        text = ""
        count = 0
        for page in doc:
            # line = page.getText().strip().encode('utf-8')
            # line = line.encode('utf-8')
            # print('\nCount=',count, 'line=', line))
            count += 1
            text += page.getText().strip()
    # print(text)

    # --- write the PDF text to a temporary text file
    textFile = open('EM_Bulletin_v01.txt', 'w', encoding='utf-8', errors='ignore')
    textFile.write(text)
    textFile.close()

    return ()


# --- End Get the current date / time

# ---- add affirmation of faith
def addaffirmation():
    import filelist
    import stringManip
    import stringsplit
    myList = []

    # -------------- Read the contents of the Affirmation of Faith text file -----------------------------
    textFile = open(filelist.AffirmationFileName, 'r', encoding='utf-8', errors='ignore')
    body_text = textFile.readlines()  # --- read the file into a list
    # print(body_text)

    slide_group_name = 'Affirmation of Faith'
    print(slide_group_name)
    # addnode.addbodytext(doctree, slide_group_name, body_text) #--- call the addbodytext function
    # --- split the text based on period '.'
    # body_text = split_keep(body_text)           #--- call my function to split the string into lines, delimited by '.'
    # body_text.insert(0, slide_group_name)       #--- insert the title at the beginning of the list

    temp_text = body_text[0] + body_text[1]
    # print('\nTemp Text=', temp_text)
    del body_text[1]  # --- remove the 1st and second list items
    del body_text[0]  # --- remove the 1st and second list items

    #body_text = stringsplit.convertListToString(body_text)     #convert the list to a string

    #print('\nAfter Call to convert List To String:\n', body_text)

    #myList = stringManip.sentenceSplit(body_text)
    #myList = stringManip.paragraphSplit(body_text)
    myList = stringManip.paragraphSplit(body_text)

    myList.insert(0, temp_text)           #---- must add back the heading lines for the Affirmation of Faith
    print('\nafter return from paragraph split\n')
    
    #print(myList)
    s = 0
    for sentence in myList:
        s += 1
        print('s=', s, 'length of sentence=', len(sentence), ' ', sentence)

    #--- end addaffirmation




def main():
    import urllib
    import writehtml
    import readworshipschedule
    import getdatetime
    import filelist
    import stringsplit
    import os

    #--- =============================
    #-------------- Read the contents of the Affirmation of Faith text file -----------------------------
    #textFile = open(filelist.AffirmationFileName, 'r', encoding='utf-8',errors='ignore')
    #body_text = textFile.read()              #--- read the file into a list
    #writehtml.buildSermonScriptureContent()
    #sys.exit(0)
    #--- ======================================
    #message_link ='https://discord.com/channels/402266274962341900/681180782240464897/832381042689048597'

    #link = message_link.split('/')
    #print(link)
    #for i in range(0, len(link)):
    #    print(i, link[i])
    # sys.exit(0)
    #test python sftp
    transferfiles()
    sys.exit(0)

    #--- ===========================
    print('\nCommitted - I think I am beginning to understand -Environment Variable:', os.getenv('TOKEN'))
    #addaffirmation()
    sys.exit(0)

    #--- =====================
    writehtml.buildSermonScriptureContent()

    sys.exit(0)
    #--- ====================

    returned_elements = maintainsong.bs4buildSetSummary('2021-03-28 GCCEM Sunday Worship')
    print(returned_elements)

    #--- convert returned list to a string separated by newlines
    print('\nafter convert to string \n')
    print('\n'.join(returned_elements))
    sys.exit(0)


    #=====================

    #import readbulletin
    #readbulletin.parsebulletin()
    #maintainsong.addsong('steves song')
    #maintainsong.updatesong('steves song')
    #maintainsong.displaysong('steves song')
    #testRenameSet()


    set_matches = maintainsong.displaySet()
    for myset, url in set_matches.items():
        print(myset, url)
 
     #opensong.assembleset()
    #opensong.cleanup()
    #readworshipschedule.readWS()
    sys.exit(0)

    #--- test mode function
    args = sys.argv[1:]
    result = ''
    for arg in args:
        result += ' ' + arg
    
    if result:
        print('\nInput arguments:', result)
    else:
        print('\nMissing song name argument')
        return()
    
    url = maintainsong.search_songs(result)
    if url == 'notfound':
        print('\nSong: {} does not exist; (song titles are case sensitive)'. format(result))
    else:
        print('\nSong Found; URL =', url)
        sys.exit(0)

    sys.exit(0)


    for arg in sys.argv[1:]:
        print('\nStart up argument=', arg)
        if 'testing' in arg:
            print('\nStart up in testing mode=', arg)
            sys.exit(0)
        else:
            song_name = arg
            urllib.parse.quote(song_name, safe='')
            url = maintainsong.displaysong(song_name)
            if 'Not Found' in url:
                print('\nSong: {} does not exist; (song titles are case sensitive)'. format(song_name))
            else:
                print('\nSong Found; URL =', url)
            sys.exit(0)

    print('\nMissing song name argument')
    sys.exit(0)

#-- end of function definition routine



# ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
#
if __name__ == "__main__":
    main()
#
# ======================================================================================

