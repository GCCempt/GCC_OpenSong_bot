# ------------ Start Build OpenSong Set function - last updated 03/02/2021 by Steve Rogers
import logging
import os

import dropbox_api_call  # --- my module to call Dropbox API
import filelist  # --- definition of list of files and directories used in the proces
import getdatetime
import sftp_files  # -- my module to call pysftp
import writehtml  # --- my module to create the HTML page with the bulletin info for the "livestream" page

set_path = 'sets/'
bulletin_path = 'bulletin/'
sample_set_path = 'sample_sets/'


# ------------ Start Assemble Set function -
def assembleset():
    import xml.etree.ElementTree as ET

    # -------------- Get the set name from the setname file -----------------------------
    textFile = open(bulletin_path + filelist.SetFilename, 'r', encoding='utf-8',
                    errors='ignore')  # --- read the file containing the selected Set name
    XMLsetName = textFile.readline()  # --- read the first line from the file
    textFile.close()

    # -------------- Open the Template Set and load into XML document tree -----------------------------
    print('\nOpenSong.assembleset() Current Working Directory:', os.getcwd())

    datasource = open(sample_set_path + XMLsetName, 'rb')

    doctree = ET.parse(datasource)
    root = doctree.getroot()
    print('\nAssembleSet - the number of slide_groups in the set: ', len(root[0]))

    # -------------- call the process files function to process the files with the extracted bulletin information
    status_message = processfiles(doctree)  # --- pass the XML set document tree

    return (status_message)


# ------------ End Assemble Set function -

# ------------Start -  Process files with extracted bulletin information
def processfiles(doctree):
    import addnode
    import processAffirmationOfFaith

    # -------------- Read the contents of the Call To Worship text file -----------------------------
    slide_group_name = 'Call to Worship'
    body_text = parsecalltoworship()  # --- call the 'parsecalltoworship' routine to separate the text into slides / list

    addnode.addbodyslides(doctree, slide_group_name, body_text)  # --- call the add confession text function

    # -------------- Read the contents of the Bulletin Sermon  text file -----------------------------
    textFile = open(bulletin_path + filelist.BulletinSermonFilename, 'r', encoding='utf-8', errors='ignore')
    body_text = textFile.read()  # --- read the file into a string
    # print(body_text)

    slide_group_name = 'Sermon'
    addnode.addbodytext(doctree, slide_group_name, body_text)  # --- call the addbodytext function

    # -- Add the Sermon Scripture to the XML document
    scripture = body_text.splitlines()
    scripture_ref = scripture[1].strip()
    #print('\nOpenSong.processfiles - Sermon Scripture Reference=', scripture_ref)
    addnode.addscripture(doctree, slide_group_name, scripture_ref)

    # -------------- Process the contents of the Confession of Sin text file -----------------------------
    slide_group_name = 'Confession of Sin'

    textFile = open(bulletin_path + filelist.ConfessionFilename, 'r', encoding='utf-8', errors='ignore')
    body_text = textFile.readlines()[1:]  # --- skip the first line and read the rest of the file into a list

    body_text.insert(0, slide_group_name)  # --- insert the title at the beginning of the list

    addnode.addbodyslides(doctree, slide_group_name, body_text)  # --- call the add body text function
    
    # -------------- Read the contents of the Assurance of Pardon text file -----------------------------
    textFile = open(bulletin_path + filelist.AssuranceFilename, 'r', encoding='utf-8', errors='ignore')
    body_text = textFile.readlines()  # --- read the file into a list

    slide_group_name = 'Assurance of Pardon'
    scripture_ref = str(body_text[1].strip())
    #print('\nScripture Reference:', scripture_ref)
    body_text = slide_group_name + '\n' + scripture_ref
    # print('\nBODY TEXT for Assurance of Pardon:\n', body_text)
    addnode.addbodytext(doctree, slide_group_name, body_text)  # --- call the addbodytext function

    addnode.addscripture(doctree, slide_group_name, scripture_ref)

    # -------------- Read the contents of the Affirmation of Faith text file -----------------------------
    slide_group_name = 'Affirmation of Faith'

    body_text = processAffirmationOfFaith.read_affirmation_of_faith()
    addnode.addbodyslides(doctree, slide_group_name, body_text)  # --- call the add body text function

    # -------------- Read the contents of the Scripture Reading text file -----------------------------
    textFile = open(bulletin_path + filelist.ScriptureFileName, 'r', encoding='utf-8', errors='ignore')
    body_text = textFile.read()  # --- read the file into a string
    body_text = body_text + '\n'

    slide_group_name = 'Scripture Reading'
    addnode.addbodytext(doctree, slide_group_name, body_text)  # --- call the addbodytext function

    # -- Add the Scripture Text to the XML document
    scripture = body_text.splitlines()
    scripture_ref = scripture[1].strip()
    # print('\nScripture Reference=', scripture_ref)
    addnode.addscripture(doctree, slide_group_name, scripture_ref)

    # -------------- Read the contents of the Announcements text file -----------------------------
    textFile = open(bulletin_path + filelist.AnnouncementFileName, 'r', encoding='utf-8', errors='ignore')
    body_text = textFile.readlines()  # --- read the file into a list

    slide_group_name = 'Announcements'
    # addnode.addbodytext(doctree, slide_group_name, body_text) #--- call the addbodytext function
    addnode.addbodyslides(doctree, slide_group_name, body_text)

    # --- Process the Worship songs-----------------------------
    processsongs(doctree)

    # --- call the write xml set function to write the new xml set file
    status_message = writeXMLSet(doctree)

    return status_message


# ------------End -  Process files with extracted bulletin information

# ------------Start -  Process Songs
def processsongs(doctree):
    import addnode
    import readworshipschedule

    # -------------- Read and process the songs text file -----------------------------
    songs = []
    songs = readworshipschedule.readWS()        #-- retrieve a list of songs and presentation orders

    # --- process the Song of Approach
    song_name = songs[1][0]
    presentation_order = songs[1][1]
    song_name, presentation_order = trim_text(song_name, presentation_order)

    slide_group_name = 'Song of Approach'
    body_text = slide_group_name
    body_text = body_text + '\n' + song_name

    doctree = addnode.addsong(doctree, slide_group_name, song_name, presentation_order)  # (slide_group_name, url)
    addnode.addbodytext(doctree, slide_group_name, body_text)

    # --- process the Song of Response - last line in the list
    song_name = songs[len(songs)-1][0]
    presentation_order = songs[len(songs)-1][1]  # split the line at '-'
    song_name, presentation_order = trim_text(song_name, presentation_order)

    slide_group_name = 'Song of Response'
    body_text = slide_group_name
    body_text = body_text + '\n' + song_name

    doctree = addnode.addsong(doctree, slide_group_name, song_name, presentation_order)  # (slide_group_name, url)
    addnode.addbodytext(doctree, slide_group_name, body_text)

    # --- process Praise Songs - order is based on the established set name
    # -------------- Get the set name form the setname file -----------------------------
    textFile = open(bulletin_path + filelist.SetFilename, 'r', encoding='utf-8',
                    errors='ignore')  # --- read the file containing the selected Set name
    XMLsetName = textFile.readline()  # --- read the first line from the file
    textFile.close()

    if 'NoGloriaPatri' in XMLsetName:  # means use 1 song of praise and a song of assurance
        song_name = songs[2][0]
        presentation_order = songs[2][1]
        song_name, presentation_order = trim_text(song_name, presentation_order)

        slide_group_name = 'Song of Praise'
        body_text = slide_group_name
        body_text = body_text + '\n' + song_name

        doctree = addnode.addsong(doctree, slide_group_name, song_name,
                                  presentation_order)  # (slide_group_name, url)
        addnode.addbodytext(doctree, slide_group_name, body_text)

        # --- Song or Assurance
        song_name = songs[3][0]
        presentation_order = songs[3][1]
        song_name, presentation_order = trim_text(song_name, presentation_order)

        slide_group_name = 'Song of Assurance'
        body_text = slide_group_name
        body_text = body_text + '\n' + song_name

        doctree = addnode.addsong(doctree, slide_group_name, song_name,
                                  presentation_order)  # (slide_group_name, url)
        addnode.addbodytext(doctree, slide_group_name, body_text)

    else:  # --- process body_text for 2 Songs of Praise
        slide_group_name = 'Songs of Praise'
        body_text = slide_group_name

        for s in range(2, len(songs) - 1):  # --- process body_text for 2 Songs of Praise
            song_name = songs[s][0]
            presentation_order = songs[s][1]
            song_name, presentation_order = trim_text(song_name, presentation_order)

            body_text = body_text + '\n' + song_name

            addnode.addbodytext(doctree, slide_group_name, body_text)

        for s in range(len(songs) - 2, 1, -1):  # --- process 2 Songs of Praise in reverse order
            song_name = songs[s][0]
            presentation_order = songs[s][1]
            song_name, presentation_order = trim_text(song_name, presentation_order)

            doctree = addnode.addsong(doctree, slide_group_name, song_name,
                                      presentation_order)  # (slide_group_name, url)
    return ()
#---  End process songs routine

# ------------Start -  extrqact song and presentation order
def trim_text(song_name, presentation_order):
    song_name = song_name.strip().rstrip('-')  # remove trailing '-'
    song_name = song_name.strip()  # remove leading and trailing spaces
    presentation_order = presentation_order.strip()  # remove leading and trailing spaces

    return(song_name, presentation_order)
# -------------- End extract song and presentation order -----------------------------

# ------------Start -  Write the new XML set
def writeXMLSet(doctree):
    from utils import generate_set_name

    set_path = 'sets/'

    setNameAttrib = generate_set_name()

    myroot = doctree.getroot()  # --- XML document tree passed as a parameter

    myroot.attrib = {'name': setNameAttrib}  # --- assign the set name attribute
    print(myroot.tag, myroot.attrib)

    # --- End of processing - write out the modified worship set

    outputset = set_path + setNameAttrib  # --- the set file name is the same as the set name
    doctree.write(outputset)

    status_message = updatefinalstatus()  # --- update the current status file upon comletion of processing

    # --- push the set to the website and to Dropbox
    file_type = 'set'
    sftp_files.pushfiles(file_type, setNameAttrib)  # --- sftp the set to the website
    dropbox_api_call.dropboxsync(file_type, setNameAttrib)  # --- sync the set to Dropbox

    # --- push the html files to the website
    if os.environ['ENVIRON'] == 'PROD' or os.environ['ENVIRON'] == 'MAINDEV':
        file_type = 'bulletin'
        sftp_files.pushfiles(file_type, filelist.HTMLBulletinFilename)  # --- sftp the bulletin.html file
        sftp_files.pushfiles(file_type, filelist.HTMLSermonScriptureFilename)  # --- sftp the sermonscripture.html file

    return status_message


# ------------End -  Write the new XML set

# ------------Start Function to split string into list by '.'
def split_keep(string):
    string = string.split('.')

    for i in range(0, len(string)):
        string[i] = string[i] + '.'
        # print(string[i])
    del string[-1]  # --- remove the last item from the list
    return string  # --- return a list of sentences with '.'


# -----------End Function to split string into list by '.'

# ------------Start Function to extract string after Nth occurrence of specified character
def split_keep_after(string, char, count):  # --- input string, delimiter, occurrence
    # print('The original string is:' + str(string))

    res = string.split(char, count)[-1]

    # print("The extracted string : " + str(res))

    return res  # --- return the remaining string


# -----------End Function to extract residual characters in string

# ------------Start Function to parse the call to worship
def parsecalltoworship():
    # -------------- Read the contents of the Call To Worship text file -----------------------------
    textFile = open(bulletin_path + filelist.CallToWorshipFileName, 'r', encoding='utf-8', errors='ignore')
    Lines = textFile.readlines()  # --- read the file into a list
    # print(body_text)
    leader_flag = ''
    congregation_flag = ''
    body_text = [Lines[0] + Lines[1]]
    # print(body_text)

    # --- determine if this is a responsive reading
    line_count = 0
    for i in Lines:
        # print(i, end = '')
        line_count += 1

        if "leader:" in i.replace(" ", '').replace('\t', '').lower():
            leader_flag = "y"  # --- set the leader flag
        elif 'congregation:' in i.replace(" ", '').replace('\t', '').lower():
            congregation_flag = 'y'  # --- set the congregation flag

    if leader_flag and congregation_flag:  # ---  this call to worship is a responsive reading
        body_text = process_responsivereading(Lines, body_text)
    else:
        line_count = 2
        for i in range(2, len(Lines)):
            body_text.append(Lines[line_count])
            line_count += 1

    return body_text
# --- end parsecalltoworship

#--- Process responsive reading
def process_responsivereading(Lines, body_text):
    from stringManip import sentenceSplit, periodSplit
    from stringsplit import convertListToString
    import re

    count = 1  # --- position the index after the header lines
    end = len(Lines)
    leader_text = ''
    congregation_text = ''
    all_text = ''

    while count < end:

        # print('\ncount=', count, 'line=', Lines[count], ' end=', end)
        # line = Lines[count].lower()

        # --- Look for responsive reading -----------------------------
        if 'leader' in Lines[count].lower():
            for j in range(count, end):
                # print('\nIn leader section - j=', j,  ' text=', Lines[j], ' end=', end)
                leader_text = leader_text + Lines[j]
                if j + 1 == end:
                    body_text.append(leader_text)
                    break
                else:
                    if 'congregation' in Lines[j + 1].lower() or 'alltogether' in Lines[j + 1].lower().replace(" ",
                                                                                                                 ''):
                        # print('\nLeader Body Text =', leader_text)
                        body_text.append(leader_text)
                        leader_text = ''
                        count = j
                        break
                j += 1

        elif "congregation" in Lines[count].lower():
            # print('\nMatched congregation section - count =', count)
            for j in range(count, end):
                congregation_text = congregation_text + Lines[j]
                if j + 1 == end:
                    body_text.append(congregation_text)
                    break
                else:
                    if 'leader' in Lines[j + 1].lower() or 'alltogether' in Lines[count + 1].lower().replace(" ", ''):
                        congregation_text = congregation_text.replace('\n', ' ')        #--- remove unwanted newline
                        #congregation_text = re.sub('(\.)\s\w', '(\.)\s\n', congregation_text)
                        #congregation_text = congregation_text.replace('.', '. \n')      #-- add newlines after each sentence
                        congregation_text = congregation_text.splitlines(True)      #--- split string based on newline
                        for line in congregation_text:
                            body_text.append(line)
                        
                        congregation_text = ''
                        count = j
                        break
                j += 1

        elif 'alltogether' in Lines[count].lower().replace(" ", ''):
            # print('\nMatched Alltogether section')
            for j in range(count, end):
                all_text = all_text + Lines[j]
                
                if j + 1 == end:
                    body_text.append(all_text)
                    break
                else:
                    if 'leader' in Lines[j + 1].lower() or 'congregation' in Lines[count + 1].lower().replace(" ", ''):
                        # print('\nCongregation Body Text =', congregation_text)
                        body_text.append(all_text)
                        all_text = ''
                        count = j
                        break

                j += 1
            # print('\nAlltogether Body Text =', all_text)
            #body_text.append(all_text)
            count = j
        count += 1

    # j = 0
    # for i in body_text:
    #    print('\nj=', j, 'line=', i)
    #    j +=1

    return body_text  # --- return the body_text array


# -----------End Function to parse call to worship

# ------------Start Function post the completion status
def updatefinalstatus():  # --- update the current status  file
    # --- read the bulletin date file
    textFile = open(bulletin_path + filelist.BulletinDateFilename, 'r', encoding='utf-8', errors='ignore')
    filedate = textFile.read()  # --- read the file into a string
    textFile.close()
    status_message = '\nBulletin Processing completed for ' + filedate

    # --- Update the current status file
    textFile = open(bulletin_path + filelist.CurrentStatusFilename, 'a', encoding='utf-8',
                    errors='ignore')  # --- append to the current status file
    textFile.write(str(status_message))
    textFile.close()

    writehtml.buildhtmlcontent()  # --- create the HTML page to be uploaded to the website

    status_date = str(getdatetime.currentdatetime())
    status_message = status_message + '\nOpenSong Set created on: ' + status_date

    print(status_message)

    return status_message  # --- return the remaining string
# -----------End Function to extract residual characters in string
