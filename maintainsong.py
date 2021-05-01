# ------------ Add new song to OpenSong
import filelist  # --- definition of list of files and directories used in the proces
import os
import getdatetime
import writehtml  # --- my module to create the HTML page with the bulletin info for the "livestream" page
import subprocess  # --- for launching external shell commands
import xml.etree.ElementTree as ET
import sys


# ------------ Start Add Song function -
def addsong(songname):
    # -------------- Read the contents of the new song lyrics into a list -----------------------------
    textFile = open(filelist.NewSongTextFilename, 'r', encoding='utf-8', errors='ignore')
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

    datasource = open(filelist.SongTemplate, 'rb')  # --- read the XML song template

    doctree = ET.parse(datasource)
    root = doctree.getroot()

    # --- Read the contents of the lyrics text file -----------------------------
    textFile = open(filelist.NewSongTextFilename, 'r', encoding='utf-8', errors='ignore')
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
    os.chdir(filelist.songpath)  # -- change to the Songs directory
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

    os.chdir(filelist.bulletinpath)  # -- change to the Bulletin directory

    # --- execute the rsync process to upload the song to the website
    subprocess.Popen(
        '/root/Dropbox/OpenSongV2/rclone-cron.sh')  # --- run the rclone sync process to upload the set to the website

    return (status_message)


# ------------ End Build Song function -

# ------------Start -  Write Song
def updatesong(songname):
    # -------------- Read the contents of the new song lyrics into a list -----------------------------
    textFile = open(filelist.NewSongTextFilename, 'r', encoding='utf-8', errors='ignore')
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

    datasource = open(filelist.SongTemplate, 'rb')  # --- read the XML song template

    doctree = ET.parse(datasource)
    root = doctree.getroot()

    # --- Read the contents of the lyrics text file -----------------------------
    textFile = open(filelist.NewSongTextFilename, 'r', encoding='utf-8', errors='ignore')
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
    os.chdir(filelist.songpath)  # -- change to the OpenSong Songs directory

    # --- check if the song already exists
    if not os.path.isfile(songname):
        status_message = 'Unable to update - this song does not exists: {} Try a different name...'.format(songname)
        print(status_message)
        return (status_message)
    else:
        # --- https://stackoverflow.com/questions/39262455/how-to-write-xml-declaration-into-xml-file
        with open(songname, 'wb') as f:
            f.write(b'<?xml version="1.0" encoding="UTF-8"?>')
            doctree.write(f, xml_declaration=False, encoding='utf-8')
            status_message = 'Song updated: {}...'.format(songname)
            print(status_message)

    os.chdir(filelist.bulletinpath)  # -- change to the Bulletin directory

    # --- execute the rsync process to upload the song to the website
    subprocess.Popen(
        '/root/Dropbox/OpenSongV2/rclone-cron.sh')  # --- run the rclone sync process to upload the set to the website

    return (status_message)


# ------------End -  Update Song function

# ------------ Start Dislay Song function -  send link to song
def displaysong(song_name):
    import urllib.request, urllib.error
    # from urllib.request import Request, urlopen, urlretrieve
    # --- Sample URL: http://gccpraise.com/os-viewer/preview_song.php?s=A%20New%20Hallelujah
    print('\nDisplaySong received song_name=', song_name)
    result = song_name.strip()  # --- strip leading and trailing whitespace
    song_name_encoded = urllib.parse.quote(result, safe='')  # ---convert string to valid URL encoded spaces
    url = 'http://gccpraise.com/os-viewer/preview_song.php?s=' + song_name_encoded

    print('\nDisplaySong url lookup = ', url)
    # --- Set Browser Agent
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    try:
        status_code = urllib.request.urlopen(req)
        print('\nDisplaySong song=', status_code.read().decode('utf-8'))
        if song_name in status_code.read().decode('utf-8'):
            # print('\nReturned status code=', status_code.read().decode('utf-8'))
            return (url)
        else:
            return ('Song Not Found')
    # except urllib.request.HTTPError:
    except urllib.error.HTTPError as e:
        status_code = '\nHTTPError: {}'.format(e.code)
        return (status_code)


# ------------ Start Search Song function -
def search_songs(query):
    from abc import ABC
    from html.parser import HTMLParser  # docs - https://docs.python.org/3/library/html.parser.html
    from urllib import parse as uparse
    from urllib.request import urlopen, Request
    from fuzzywuzzy import fuzz

    # Directory we're checking
    url = 'http://gccpraise.com/opensongv2/xml/'
    # Wordpress will deny the python urllib user agent, so we set it to Mozilla.
    page = urlopen(Request(url, headers={'User-Agent': 'Mozilla'}))
    # Read the content and decode it
    content = page.read().decode()
    # Initialize empty list for songs.
    song_list = []
    # URL Prefix
    prefix = "http://gccpraise.com/os-viewer/preview_song.php?s="
    # a number which ranges from 0 to 100, this is used to set how strict the matching needs to be
    threshold = 80

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
                        song_list.append(link)

    # Create a new parse object.
    directory_parser = Parse()
    # Call feed method. incomplete data is buffered until more data is fed or close() is called.
    directory_parser.feed(content)
    # format the URL list by replacing the HTML safe %20
    song_list = [song.replace("%20", " ") for song in song_list]
    # TODO: Remove test query
    # query = "the King of Heaven"
    # Build empty dictionary to add matches to.
    matches = {}
    # Check the match ratio on each song in the song list. This is expensive using pure-python.
    for song in song_list:
        if fuzz.partial_ratio(song, query) >= threshold:
            song_name = song.replace("%20", " ")
            song = uparse.quote(song, safe='')
            song = prefix + song
            matches[song_name] = song
    
    return(matches)


# ------------ Start Dislay Set function -  send link to song
def displaySet(setDate=str(getdatetime.nextSunday())):  # --- get a default date; will be overriden if date is passed
    from abc import ABC
    from html.parser import HTMLParser  # docs - https://docs.python.org/3/library/html.parser.html
    from urllib import parse as uparse
    from urllib.request import urlopen, Request
    from fuzzywuzzy import fuzz
    import urllib
    import getdatetime  # --- my module for date calculation / generation

    # setDate = str(getdatetime.nextSunday())         #--- get next Sunday date to build the set name
    # print('\nUsing default date of this Sunday=', setDate)

    query = setDate  # --  this is the fuzzy varible for the the set search
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
    print('\nBS4BuildSetSummary - SetName=', SetName)
    # setpath = '/root/Dropbox/OpenSongV2/OpenSong Data/Sets'
    print('\nSetpath=', filelist.setpath)

    # -------------- Open the Template Set and load into XML document tree -----------------------------
    wk_dir = os.getcwd()
    print('\nStart BS4BuildSetSummary - current working directory: ', wk_dir)
    if 'bulletin' in wk_dir:
        os.chdir('../sets')  # -- change to the Sets directory
        print('\nBS4BuildSetSummary - changed working directory: ', os.getcwd())

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
