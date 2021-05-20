# ------------ Add new song to OpenSong
import os
import subprocess  # --- for launching external shell commands
import xml.etree.ElementTree as ET

import filelist  # --- definition of list of files and directories used in the proces
import getdatetime

set_path = 'sets/'
bulletin_path = 'bulletin/'
song_path = 'songs/'
# ------------ Start Add Song function -
def addsong(songname):
    # -------------- Read the contents of the new song lyrics into a list -----------------------------
    textFile = open(bulletin_path + filelist.NewSongTextFilename, 'r', encoding='utf-8', errors='ignore')
    Lines = textFile.readlines()  # --- read the file into a list

    # --- ensure the text lines start with ' '; other lines remain as is
    i = 0
    for line in Lines:
        if line[0] == '.' or line[0] == ' ' or line[0] == '[':
            Lines[i] = line
        else:
            line = ' ' + line
            Lines[i] = line
        i += 1
    # print(Lines)
    lyrics_text = ''.join(Lines)
    # print(lyrics_text)

    # --- Open the Template Song and load into XML document tree -----------------------------
    print('\nMaintainSong.buildsong() ', songname, 'Current Working Directory:', os.getcwd())

    datasource = open(song_path + filelist.SongTemplate, 'rb')  # --- read the XML song template

    doctree = ET.parse(datasource)
    root = doctree.getroot()

    # --- Read the contents of the lyrics text file -----------------------------
    textFile = open(bulletin_path + filelist.NewSongTextFilename, 'r', encoding='utf-8', errors='ignore')
    newsong_lyrics = textFile.read()  # --- read the file into a string

    root = doctree.getroot()
    # --- add the lyrics to the song template
    for lyrics in root.iter('lyrics'):
        lyrics.text = lyrics_text

    for title in root.iter('title'):
        title.text = songname

    for child in root:
        print(child.tag, child.attrib, child.text)

    # --- write the new song to the OpenSong songs folder
    os.chdir(song_path + filelist.songpath)  # -- change to the Songs directory
    # --- check if the song already exists
    if os.path.isfile(songname):
        status_message = 'This song already exists: {} Try a different name...'.format(songname)
        # print("This song already exists: {} Try a different name...".format(songname))
        print(status_message)
        return (status_message)
    else:
        # doctree.write(songname, xml_declaration=True)
        # --- https://stackoverflow.com/questions/39262455/how-to-write-xml-declaration-into-xml-file
        with open(songname, 'wb') as f:
            f.write(b'<?xml version="1.0" encoding="UTF-8"?>')
            doctree.write(f, xml_declaration=False, encoding='utf-8')
            status_message = 'New Song created: {}...'.format(songname)
            # print("New Song created: {}...".format(songname))
            print(status_message)

    # --- execute the rsync process to upload the song to the website
    subprocess.Popen(
        '/root/Dropbox/OpenSongV2/rclone-cron.sh')  # --- run the rclone sync process to upload the set to the website

    return (status_message)


# ------------ End Build Song function -

# ------------Start -  Write Song
def updatesong(songname):
    # -------------- Read the contents of the new song lyrics into a list -----------------------------
    textFile = open(song_path + filelist.NewSongTextFilename, 'r', encoding='utf-8', errors='ignore')
    Lines = textFile.readlines()  # --- read the file into a list

    # --- ensure the text lines start with ' '; other lines remain as is
    i = 0
    for line in Lines:
        if line[0] == '.' or line[0] == ' ' or line[0] == '[':
            Lines[i] = line
        else:
            line = ' ' + line
            Lines[i] = line
        i += 1
    # print(Lines)
    lyrics_text = ''.join(Lines)
    # print(lyrics_text)

    # --- Open the Template Song and load into XML document tree -----------------------------
    print('\nMaintainSong.buildsong() ', songname, 'Current Working Directory:', os.getcwd())

    datasource = open(bulletin_path + filelist.SongTemplate, 'rb')  # --- read the XML song template

    doctree = ET.parse(datasource)
    root = doctree.getroot()

    # --- Read the contents of the lyrics text file -----------------------------
    textFile = open(bulletin_path + filelist.NewSongTextFilename, 'r', encoding='utf-8', errors='ignore')
    newsong_lyrics = textFile.read()  # --- read the file into a string

    root = doctree.getroot()
    # --- add the lyrics to the song template
    for lyrics in root.iter('lyrics'):
        lyrics.text = lyrics_text

    for title in root.iter('title'):
        title.text = songname

    for child in root:
        print(child.tag, child.attrib, child.text)

    # --- write the new song to the OpenSong songs folder

    # --- check if the song already exists
    if not os.path.exists(song_path + songname):
        status_message = 'Unable to update - this song does not exists: {} Try a different name...'.format(songname)
        print(status_message)
        return (status_message)
    else:
        # --- https://stackoverflow.com/questions/39262455/how-to-write-xml-declaration-into-xml-file
        with open(song_path + songname, 'wb') as f:
            f.write(b'<?xml version="1.0" encoding="UTF-8"?>')
            doctree.write(f, xml_declaration=False, encoding='utf-8')
            status_message = 'Song updated: {}...'.format(songname)
            print(status_message)

    # --- execute the rsync process to upload the song to the website
    subprocess.Popen(
        '/root/Dropbox/OpenSongV2/rclone-cron.sh')  # --- run the rclone sync process to upload the set to the website

    return (status_message)


# ------------End -  Update Song function


# ------------ Start Search Song function -


# ------------ Start Dislay Set function -  send link to song
def displaySet(setNameAttrib=str(getdatetime.nextSunday())):  # --- get a default date; will be overriden if date is passed
    from abc import ABC
    from html.parser import HTMLParser  # docs - https://docs.python.org/3/library/html.parser.html
    from urllib import parse as uparse
    from urllib.request import urlopen, Request
    from fuzzywuzzy import fuzz
    from utils import generate_set_name

    setNameAttrib = generate_set_name()

    query = setNameAttrib  # --  this is the fuzzy varible for the the set search
    print('\nSet Lookup date=', query)

    # Directory we're checking
    url = 'http://gccpraise.com/opensongv2/sets/?s='
    # Wordpress will deny the python urllib user agent, so we set it to Mozilla.
    page = urlopen(Request(url, headers={'User-Agent': 'Mozilla'}))
    # Read the content and decode it
    content = page.read().decode()
    # Initialize empty list for songs.
    set_list = []
    # URL Prefix
    prefix = "http://gccpraise.com/os-viewer/publish_set.php?s="
    # a number which ranges from 0 to 100, this is used to set how strict the matching needs to be
    threshold = 95

    # Subclass/Override HTMLParser and define the methods we need to change.
    class Parse(HTMLParser, ABC):
        def __init__(self):
            # Since Python 3, we need to call the __init__() function of the parent class
            super().__init__()
            self.reset()

        # override handle_starttag method to only return the contents of anchor tags as a searchable list.
        def handle_starttag(self, tag, attrs):
            # Only parse the 'anchor' tag.
            if tag == "a":
                for name, link in attrs:
                    if name == "href":
                        set_list.append(link)

    # Create a new parse object.
    directory_parser = Parse()
    # Call feed method. incomplete data is buffered until more data is fed or close() is called.
    directory_parser.feed(content)
    # format the URL list by replacing the HTML safe %20
    set_list = [myset.replace("%20", " ") for myset in set_list]
    # TODO: Remove test query
    # query = "2021-04-04"
    # Build empty dictionary to add matches to.
    matches = {}
    # Check the match ratio on each song in the song list. This is expensive using pure-python.
    for myset in set_list:
        if fuzz.partial_ratio(myset, query) >= threshold:
            set_name = myset.replace("%20", " ")
            myset = uparse.quote(myset, safe='')
            myset = prefix + myset
            matches[set_name] = myset
    return matches


# ------------ end DisplaySet

# ------------ Use Beautiful Soup to extract summary of OpenSong XML Set
def bs4buildSetSummary(SetName='2021-04-04 GCCEM Sunday Worship'):
    import os
    from bs4 import BeautifulSoup
    import xml.etree.ElementTree as ET

    worship_elements = []
    display_elements = []
    SetName = SetName.lstrip()
    SetName = SetName.rstrip()
    SetName = SetName.replace('%20', '@')

    setpath = 'sets/'

    # -------------- Open the Template Set and load into XML document tree -----------------------------
    SetName = setpath + SetName
    print('\nBS4BuildSetSummary - SetName=', SetName)

    # --- test finding the set file
    datasource = open(SetName, 'rb')

    doctree = ET.parse(datasource)
    root = doctree.getroot()
    print('\nBS4BuildSet - the number of slide_groups in the set: ', len(root[0]))

    # try:
    fd = open(SetName, 'r')
    xml_file = fd.read()
    soup = BeautifulSoup(xml_file, 'lxml')

    # except:
    #    status_code ='\nError - Set Not Found: {}'. format(SetName)
    #    return(status_code)

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

    return (returned_elements)

# --- end bs4 build Set Summary
