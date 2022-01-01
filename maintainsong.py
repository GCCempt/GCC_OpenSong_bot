# ------------ Add new song to OpenSong
import os
import logging
from stringsplit import convertListToStringWithNewLine
import subprocess  # --- for launching external shell commands
import xml.etree.ElementTree as ET

import filelist  # --- definition of list of files and directories used in the proces
import getdatetime
import dropbox_api_call

# TODO: These should be variables from filelist.py
set_path = 'sets/'
bulletin_path = 'bulletin/'
song_path = 'songs/'
new_song_path = bulletin_path + filelist.NewSongTextFilename


# ------------Start -  Add Song - copy song from Dropbox to website
def addsong(song_name):
    import dropbox_api_call
    import sftp_files
    song_dir = 'songs/'

    status_message, file_name = dropbox_api_call.dropboxread('song', song_name)        #--- download song from Dropbox
    if 'file downloaded' in status_message:
        song_name = file_name   #--- convert the song_name to the validated file metadata from DropBox
        song_path = song_dir + song_name

        #--- remove the temporary copy of the file in the local directory
        if os.path.exists(song_path):
            try:
                os.remove(song_path)
                print('\nTemporary Song removed: ', song_path)
            except OSError as e:
                logging.warning(e)
                print('\nUnable to remove file: ', song_path)
    else:
        status_message = '\nError - no matching song found', song_name
    
    return(status_message)
# ------------End -  Update Song function


# ------------Start -  Sync DrobBox to Website
def dropbox_website_sync(item_name):
    import requests
    url = "https://gccpraise.com/update.php"
    res = requests.get(url)
    if res.status_code == 200:
        status_message = '\nDropbox successfully synced to website: {}!'.format(item_name)
    else:
        status_message = '\nDropbox sync to website failed: {}!'.format(item_name)
    
    print(status_message)
    return(status_message)

# ------------End -  DropBox and Website Sync

# ------------Start -  updateSet - copy set from Dropbox to website
def updateset(set_name):
    import dropbox_api_call
    import sftp_files

    set_dir = 'sets/'
    set_path = set_dir + set_name

    error_message = 'not_found'

    status_message = dropbox_api_call.dropboxread('set', set_name)        #--- download song from Dropbox
    if error_message in status_message[0]:
        return(status_message)

    #--- push set to website if there is no error from DropBox
    sftp_files.pushfiles('set', set_name)  # --- sftp the set to the website

    status_message = '\nSet successfully uploaded to website: {}!'.format(set_name)
    print(status_message)

    #--- remove the temporary copy of the file in the local directory
    if os.path.exists(set_path):
        try:
            os.remove(set_path)
            print('\nTemporary Set removed: ', set_path)
        except OSError as e:
            logging.warning(e)
            print('\nUnable to remove file: ', set_path)
    
    return(status_message)
# ------------End -  UpdateSet function

# ------------ Start Dislay Set function -  return URL link to set
def displaySet(setNameAttrib):   
    import urllib.parse 
    
    set_name_enc = urllib.parse.quote(setNameAttrib)    #urlencode the SetName
    set_url = "https://gccpraise.com/publish_set.php?s=" + set_name_enc
    
    print(set_url)
    return(set_url)

# ------------End -  DisplaySet function

# ------------ Start check if Set exists - return status code
def isSetExists(setNameAttrib):   
    import requests
    
    set_name_enc = displaySet(setNameAttrib)    #urlencode the SetName
    set_url = "https://gccpraise.com/publish_set.php?s=" + set_name_enc
    res = requests.get(set_url)

    if res.status_code == 200:
           status_message = '\nStatus 200: Set found on website: {}!'.format(set_url)
    else:
        status_message = '\nSet does not exist on website: {}!'.format(set_url)

    print(set_url)
    return(set_url)

# ------------End -  check if Set exists

# ------------ Use Beautiful Soup to extract summary of OpenSong XML Set
def bs4buildSetSummary(SetName='2021-04-04 GCCEM Sunday Worship'):
    from bs4 import BeautifulSoup
    import xml.etree.ElementTree as ET
    from stringsplit import convertListToString
    import dropbox_api_call
    from sftp_files import getfiles

    worship_elements = []
    display_elements = []
    SetName = SetName.lstrip()
    SetName = SetName.rstrip()
    SetName = SetName.replace('%20', '@')

    setpath = 'sets/'

    # -------------- Open the Template Set and load into XML document tree -----------------------------
    local_set_name = setpath + SetName
    print('\nBS4BuildSetSummary - SetName=', SetName)

    # --- test finding the set in the local sets directory
    try:
        datasource = open(local_set_name, 'rb')
    except:     #--- if the set is not found locally, try Dropbox
        error_message = 'not_found'

        #--- pull song to website if not found locally
        status_message = getfiles('set', SetName)  # --- sftp the set from the website
        #status_message = dropbox_api_call.dropboxread('set', SetName)  #--- download song from Dropbox
        if error_message in status_message[0]:
            status_message ='\nError - Set Not Found: {}'. format(SetName)
            return(status_message)
        else:
            # --- test again opening the set in the local sets directory
            try:
                datasource = open(local_set_name, 'rb')
            except:     #--- if the set is not found locally, try Dropbox
                status_message = 'Set not_found'
                return(status_message)

    doctree = ET.parse(datasource)
    root = doctree.getroot()
    #print('\nBS4BuildSet - the number of slide_groups in the set: ', len(root[0]))
   
    fd = open(local_set_name, 'r', errors='ignore')
    xml_file = fd.read()
    soup = BeautifulSoup(xml_file, 'lxml')

    slide_groups = soup.find_all('slide_group')
    # os_body = soup.find_all('body')

    for slides in slide_groups:
        slide = slides.find('slide')
        # body = slide.find('body')
        # body_text = [i.text for i in body_slide]
        # print(slide)
        if slide == None:
            pass
        else:
            # print(slide.text)
            worship_elements.append(slide.text)
    fd.close()  # --- close the xml file

    i = 0
    LIST_OF_ELEMENTS = ['calltoworship', \
                        'songofapproach', 'songsofpraise', 'songofpraise', 'songofassurance', \
                        'songofresponse', 'assuranceofpardon', 'scripturereading', 'sermon']
    # print(LIST_OF_ELEMENTS)
    num_elements = len(worship_elements)
    for i in range(0, num_elements):
        check_element = worship_elements[i].lower().replace(' ', '').replace('\n', '@').strip().lstrip('@')
        check_element = check_element.split('@', 1)
        check_element = check_element[0]
        # print('\nWorhsip element=', worship_elements[i])
        # print('\nCheckElement =', check_element)
        if check_element in LIST_OF_ELEMENTS:
            # print('\nMatched worhsip element=', worship_elements[i])
            display_elements.append(worship_elements[i])
        elif 'sermon' in check_element:
            # print('\nSermon Found=', worship_elements[i])
            display_elements.append(worship_elements[i])

    returned_elements = []
    i = 0
    for display_element in display_elements:
        i += 1
        display_element = display_element.lstrip('\n').lstrip()
        display_element = display_element.replace('\n', ': ')
        display_element = display_element.rstrip(' :')
        display_element = str(i) + ' ' + display_element
        returned_elements.append(display_element)

    set_summary = convertListToStringWithNewLine(returned_elements)  #--- convert the list of elements to a string
    return set_summary

# --- end bs4 build Set Summary
