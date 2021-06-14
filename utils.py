# Utility functions that could be re-used elsewhere
import datetime
import logging
import os
import re
from abc import ABC
from html.parser import HTMLParser
from random import randint, choice
from urllib import parse, request

import discord
import names


def parse_songs_from_file(worship_schedule):
    """
    Parses the worshipSchedule.txt and creates a python list of the song names.

    :param worship_schedule: The filename of worship schedule
    :return: python list of song names.
    """

    with open(worship_schedule) as file:
        worship_text = file.readlines()
    # Find the line with songs in the array. Assume everything after is a song per line.
    formatted_song_list = "No songs found."

    for index, line in enumerate(worship_text):
        if 'songs' in line.lower():
            song_start = index
            formatted_song_list = []
            for index2, song in enumerate(worship_text):
                # Build a list of elements after "Songs" is found.
                if "Hymn:" in song:
                    if song.startswith("Hymn:"):
                        stripped_song = song.rsplit("-", 1)
                        stripped_song = stripped_song[0].strip("Hymn:")
                        formatted_song_list.append(stripped_song.strip())
                if index2 > song_start:
                    stripped_song = song.rsplit("-", 1)
                    stripped_song = stripped_song[0].strip("* ")
                    formatted_song_list.append(stripped_song)

    if len(formatted_song_list) <= 1:
        logging.warning("Not enough sounds were found when parsing {file}".format(file=worship_schedule))
        logging.warning(worship_text)
        return "Not enough songs have were found.."
    else:
        return formatted_song_list


# Takes in a list of songs.
def validate_songs(song_list, limit):
    """
    Performs a case-insensitive check on the given dictionary to find matching
    if the passed songs have any matching keys in the dict.

    :param song_list: A python list of song names to check.
    :param limit: The maximum number of song suggestions to return
    :return: dict with 2 keys; embed data objects to be used with discord.py's embed send and
    a success/fail message. You must iterate through the embed dict to send all the messages.
    """
    url_to_search = 'http://gccpraise.com/opensongv2/xml/'
    invalid_songs = []
    valid_songs = []
    source_data = generate_link_dict(url_to_search)
    embed_messages = {}
    # convert all dictionary keys to lowercase.
    source_data_lower = {k.lower(): v for k, v in source_data.items()}
    # find an exact match within the dictionary.
    for song in song_list:

        if source_data_lower.get(song.lower()) is None:
            invalid_songs.append(song)
        else:
            song_index = list(source_data_lower.keys()).index(song.lower())
            correct_song_names = list(source_data.keys())
            valid_songs.append(correct_song_names[song_index])

    # Search for matches to build discord message.

    for index, song in enumerate(invalid_songs):
        results = search_songs(song)
        # A Dictionary of Dictionaries
        if not results:
            embed_data = discord.Embed(title="Song \'" + song + "\' not found.", color=0xe74c3c,
                                       description="We weren't able to find any similar songs.")
        else:
            embed_data = discord.Embed(title="Song \'" + song + "\' not found.", color=0xe74c3c,
                                       description="Did you mean one of these?")
        for index_num, song_result in enumerate(results, 1):
            if index_num < limit:
                embed_data = embed_data.add_field(name=song_result, value=results[song_result], inline=False)
        embed_messages[song] = embed_data

    if not invalid_songs:
        embed_messages['No Errors'] = discord.Embed(title="All Songs are Valid!", color=0x2ecc71)

    return_dict = {
        "embed": embed_messages,
        "songs": valid_songs
    }
    return return_dict


def generate_link_dict(url):
    """
    Creates a list of all links on a given page.

    :param url: The url of the page to check.
    :return: returns a dictionary of hyperlinks and their associated text.
    """
    log_message = 'URL to search received=' + url
    logging.info(log_message)

    index_url = url
    # Some sites may deny python headers so we set it to Mozilla.
    page = request.urlopen(request.Request(index_url, headers={'User-Agent': 'Mozilla'}))
    # Read the content and decode it
    content = page.read().decode()
    # Initialize empty list for links.
    link_list = []

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
                        link_list.append(link)

    # Create a new parse object.
    page_parser = Parse()
    # Call feed method. incomplete data is buffered until more data is fed or close() is called.
    page_parser.feed(content)
    # format the URL list by replacing the HTML safe %20
    link_list = [my_set.replace("%20", " ") for my_set in link_list]
    page_links = {}
    for link in link_list:
        set_name = link.replace("%20", " ")
        link = parse.quote(link, safe='')
        link = index_url + link
        page_links[set_name] = link

    return page_links


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

    return matches


def song_case_correction(song_file, song_list):
    """
    Reads the input file, checks to see if the case-insensitive names of any songs from song_list
    can be found, then updates the text file to match the case given in song_list.
    :param song_file: The name/path of the text file to update.
    :param song_list: A list of the songs to be updated with correct case in the file.
    :return: None
    """
    with open(song_file, 'r') as file:
        file_text = file.readlines()
        file.close()

    for index, line in enumerate(file_text):
        for song in song_list:
            if song.lower() in line.lower():
                file_text[index] = re.sub(song, song, file_text[index], flags=re.IGNORECASE)
                logging.warning("Updating the song-case of " + song)
    with open(song_file, 'w') as file:
        file.writelines(file_text)
        file.close()

    return None


# --- ensure proper formatting of scripture references
def parse_passages(input_passages):  # --- input is a scripture reference string
    full_ref_passages = []  # --- list to hold the complete scripture references

    passages = input_passages.replace(',', ';')  # --- standardize ';' as scripture separator
    passages = passages.strip().split(';')  # --- split the string into an array

    # --- get book, chapter, verse
    hold_book_chapter = ''  # -- save the book and chapter reference
    book = ''
    chapter = ''
    scripture = ''
    for p in passages:
        p = p.strip()
        if ' ' in p:  # --- indicates a references includes book; e.g. 'john '
            if ':' in p:  # --- indicates a complete references includes book; e.g. 'john 3:'
                book_chapter, verse = p.split(':', 1)
                book, chapter = book_chapter.split(' ', 1)
                hold_book_chapter = book_chapter.strip()  # --- remove leading and trailing spaces
                passage_ref = hold_book_chapter + ':' + verse
                full_ref_passages.append(passage_ref)
            else:
                passage_ref = hold_book_chapter + ':' + verse
                full_ref_passages.append(passage_ref)
                book, chapter = hold_book_chapter.split(' ', 1)
        else:
            if ':' in p:  # --- no book; just chapter and verse(s), e.g. 5:1-3
                passage_ref = book + ' ' + p
                full_ref_passages.append(passage_ref)
                book_chapter, ref = passage_ref.split(':', 1)
                hold_book_chapter = str(book_chapter) + ':'

            else:
                verse = p
                passage_ref = hold_book_chapter + ':' + verse
                full_ref_passages.append(passage_ref)
                book_chapter, ref = passage_ref.split(':', 1)
                # hold_book_chapter = str(book_chapter) + ':'
    return full_ref_passages


def generate_song_name():
    song_dict = generate_link_dict("http://gccpraise.com/opensongv2/xml/")
    # Generate a Song
    if '/opensongv2/' in song_dict:
        song_dict.pop('/opensongv2/')
    keys = list(song_dict.keys())
    song_suffix = ' -'
    chars = ['V', 'C', 'T', 'B', 'E', 'X', 'P', 'O', 'I']
    # Generate pseudo-random opensong stuff
    for char in range(randint(4, 8)):
        song_suffix += " " + choice(chars) + str(randint(0, 9))
    song_name = choice(keys) + song_suffix
    # Reset the suffix
    suffix = ' -'

    return song_name


def generate_random_worship_schedule(filename):
    # Get a random date.
    date = (datetime.date.today() + datetime.timedelta(randint(1, 1000))).strftime("%m/%d/%y")
    text = "Worship Schedule " + str(date) + "\n\n"
    prefix = ["Mr.", "Mrs", "Ms.", "Dr.", "Pastor"]
    text += "Worship Leader: " + choice(prefix) + " " + names.get_full_name() + "\n"
    text += "Speaker: " + choice(prefix) + " " + names.get_full_name() + "\n"
    text += "Hymn: " + generate_song_name() + "\n"
    text += "\n"
    text += "Praise Team\n"
    text += choice(prefix) + " " + names.get_first_name() + ", " + names.get_first_name() + "\n"
    text += "\n"
    text += "Computer: " + choice(prefix) + " " + names.get_last_name() + "\n"
    text += "Sound: " + names.get_first_name() + "\n"
    text += "Camera: " + names.get_first_name() + "\n"
    text += "\n"
    text += "Songs\n"
    # Finish with random number of songs
    for number in range(randint(1, 5)):
        text += "* " + generate_song_name() + "\n"
    f = open(filename, 'w')
    f.writelines(text)
    f.close()
    return filename


# --- generate the OpenSong Set name to be used by various functions
def generate_set_name():
    from getdatetime import nextSunday, getDayOfWeek, currentdatetime

    # get the environment variables
    runtime_env = os.environ['ENVIRON']
    computer_name = os.environ['COMPUTERNAME']
    cut_off_time = '11:00'
    current_time = currentdatetime(dateformat='%H:%M')
    current_date = currentdatetime(dateformat='%Y-%m-%d')

    # --- TESTING BLOCK
    # runtime_env = 'PROD'
    # current_time = '10:45'
    # --- END TESTING BLOCK

    if runtime_env == 'PROD':
        # check current date / time; if Sunday before 11:00 use "today's" date instead of Next Sunday
        today = getDayOfWeek()
        if today == 'Sunday' and current_time < cut_off_time:
            setNameAttrib = current_date  # --- get today's date
        else:
            setNameAttrib = str(nextSunday())  # --- get the "upcoming" Sunday date
    else:  # --- running in TEST
        setNameAttrib = computer_name  # --- set default dummy set name for NON-PROD environments

    setname = setNameAttrib + ' GCCEM Sunday Worship'

    return (setname)  # --- return the generated set name

    # --- routine to write message files generated by Discord Posts


def write_message_file(message_text, file_name):
    bulletin_path = 'bulletin/'

    textFile = open(bulletin_path + file_name, 'w', encoding='utf-8', errors='ignore')
    textFile.writelines(message_text)
    textFile.close()
    return ()


# --- end write message file routine

# --- read ahead routine
def read_ahead(my_list):
    for item in my_list:
        yield (item)
    yield (None)


# --- Parse the incoming Discord message
def parsemessage():
    import filelist

    bulletin_path = 'bulletin/'
    status_message = []
    valid_message = ''

    try:
        # --- Read the Discord message file
        textFile = open(bulletin_path + filelist.DiscordMessageFilename, 'r', encoding='utf-8', errors='ignore')
        Lines = textFile.readlines()  # --- read the file into a list
        # line = textFile.read()  # --- read the file into a list
        textFile.close()
    except:
        file_status = "Discord Message file {} does not exist. Unable to process messages...".format(
            bulletin_path + filelist.DiscordMessageFilename)
        status_message.append(file_status)
        return (status_message)

    # --- process the file
    items = read_ahead(Lines)
    item = items.__next__()  # -- get the first line

    while (item):
        if item == None:
            break

        if 'sermoninfo' in item.replace(" ", '').replace('\t', '').lower():
            message_text = ''
            status_message.append('\nSermon Information received')

            while (item):
                message_text = message_text + item
                next_line = items.__next__()

                if next_line == None:
                    # print(message_text)
                    # print('\end of sermon info text')
                    write_message_file(message_text, filelist.SermonInfoFilename)
                    item = next_line
                    break

                if 'confessionofsin' in next_line.replace(" ", '').replace('\t',
                                                                           '').lower() or 'assuranceofpardon' in next_line.replace(
                    " ", '').replace('\t', '').lower():  # --- get the next item
                    # print(message_text)
                    # print('\end of sermon info text')
                    write_message_file(message_text, filelist.SermonInfoFilename)
                    item = next_line  # -- get the next item
                    break

                item = next_line  # -- get the next item

        elif item != None and 'confessionofsin' in item.replace(" ", '').replace('\t', '').lower():
            message_text = ''
            status_message.append('\nConfession of Sin receoved')

            while (item):
                message_text = message_text + item
                next_line = items.__next__()

                if next_line == None:
                    # print(message_text)
                    # print('\end of confession of sin text')
                    write_message_file(message_text, filelist.ConfessionFilename)
                    item = next_line
                    break

                if 'sermoninfo' in next_line.replace(" ", '').replace('\t',
                                                                      '').lower() or 'assuranceofpardon' in next_line.replace(
                    " ", '').replace('\t', '').lower():  # --- get the next item
                    # print(message_text)
                    # print('\end of confession of sin text')
                    write_message_file(message_text, filelist.ConfessionFilename)
                    item = next_line  # -- get the next item
                    break

                item = next_line  # -- get the next item

        elif item != None and 'assuranceofpardon' in item.replace(" ", '').replace('\t', '').lower():
            message_text = ''
            status_message.append('\nAssurance of Pardon received')

            while (item):
                message_text = message_text + item
                next_line = items.__next__()

                if next_line == None:
                    # print(message_text)
                    # print('\end of assurance of pardon text')
                    write_message_file(message_text, filelist.AssuranceFilename)
                    item = next_line
                    break

                if 'sermoninfo' in next_line.replace(" ", '').replace('\t', '').lower() or \
                        'confessionofsin' in next_line.replace(
                    " ", '').replace('\t', '').lower():  # --- get the next item
                    # print(message_text)
                    # print('\end of assurance of pardon text')
                    write_message_file(message_text, filelist.AssuranceFilename)
                    item = next_line  # -- get the next item
                    break

                item = next_line  # -- get the next item

        elif item != None and 'worshipschedule' in item.replace(" ", '').replace('\t', '').lower():
            message_text = ''
            status_message.append('\nWorship Schedule received')

            while (item):
                message_text = message_text + item
                next_line = items.__next__()

                if next_line == None:
                    # print(message_text)
                    # print('\end of worship schedule text')
                    write_message_file(message_text, filelist.WorshipScheduleFilename)
                    item = next_line

                    break
                else:
                    item = next_line

            item = next_line  # -- get the next item

        else:
            item = items.__next__()  # --- skip unrecognized line

    if len(status_message) == 0:  # --- no valid message received
        status_message.append('\nUnrecognized message received')

    return (status_message)
    # --- end Parse the incoming Discord message
    return (setname)  # --- return the generated set name

    # --- routine to write message files generated by Discord Posts


def write_message_file(message_text, file_name):
    bulletin_path = 'bulletin/'

    textFile = open(bulletin_path + file_name, 'w', encoding='utf-8', errors='ignore')
    textFile.writelines(message_text)
    textFile.close()
    return ()


# --- end write message file routine

# --- read ahead routine
def read_ahead(my_list):
    for item in my_list:
        yield (item)
    yield (None)


# --- Parse the incoming Discord message
def parsemessage():
    import filelist

    bulletin_path = 'bulletin/'
    status_message = []
    valid_message = ''

    try:
        # --- Read the Discord message file
        textFile = open(bulletin_path + filelist.DiscordMessageFilename, 'r', encoding='utf-8', errors='ignore')
        Lines = textFile.readlines()  # --- read the file into a list
        # line = textFile.read()  # --- read the file into a list
        textFile.close()
    except:
        file_status = "Discord Message file {} does not exist. Unable to process messages...".format(
            bulletin_path + filelist.DiscordMessageFilename)
        status_message.append(file_status)
        return (status_message)

    # --- process the file
    items = read_ahead(Lines)
    item = items.__next__()  # -- get the first line

    while (item):
        if item == None:
            break

        if 'sermoninfo' in item.replace(" ", '').replace('\t', '').lower():
            message_text = ''
            status_message.append('\nSermon Information received')

            while (item):
                message_text = message_text + item
                next_line = items.__next__()

                if next_line == None:
                    # print(message_text)
                    # print('\end of sermon info text')
                    write_message_file(message_text, filelist.SermonInfoFilename)
                    item = next_line
                    break

                if 'confessionofsin' in next_line.replace(" ", '').replace('\t',
                                                                           '').lower() or 'assuranceofpardon' in next_line.replace(
                    " ", '').replace('\t', '').lower():  # --- get the next item
                    # print(message_text)
                    # print('\end of sermon info text')
                    write_message_file(message_text, filelist.SermonInfoFilename)
                    item = next_line  # -- get the next item
                    break

                item = next_line  # -- get the next item

        elif item != None and 'confessionofsin' in item.replace(" ", '').replace('\t', '').lower():
            message_text = ''
            status_message.append('\nConfession of Sin receoved')

            while (item):
                message_text = message_text + item
                next_line = items.__next__()

                if next_line == None:
                    # print(message_text)
                    # print('\end of confession of sin text')
                    write_message_file(message_text, filelist.ConfessionFilename)
                    item = next_line
                    break

                if 'sermoninfo' in next_line.replace(" ", '').replace('\t',
                                                                      '').lower() or 'assuranceofpardon' in next_line.replace(
                    " ", '').replace('\t', '').lower():  # --- get the next item
                    # print(message_text)
                    # print('\end of confession of sin text')
                    write_message_file(message_text, filelist.ConfessionFilename)
                    item = next_line  # -- get the next item
                    break

                item = next_line  # -- get the next item

        elif item != None and 'assuranceofpardon' in item.replace(" ", '').replace('\t', '').lower():
            message_text = ''
            status_message.append('\nAssurance of Pardon received')

            while (item):
                message_text = message_text + item
                next_line = items.__next__()

                if next_line == None:
                    # print(message_text)
                    # print('\end of assurance of pardon text')
                    write_message_file(message_text, filelist.AssuranceFilename)
                    item = next_line
                    break

                if 'sermoninfo' in next_line.replace(" ", '').replace('\t',
                                                                      '').lower() or 'confessionofsin' in next_line.replace(
                    " ", '').replace('\t', '').lower():  # --- get the next item
                    # print(message_text)
                    # print('\end of assurance of pardon text')
                    write_message_file(message_text, filelist.AssuranceFilename)
                    item = next_line  # -- get the next item
                    break

                item = next_line  # -- get the next item

        elif item != None and 'worshipschedule' in item.replace(" ", '').replace('\t', '').lower():
            message_text = ''
            status_message.append('\nWorship Schedule received')

            while (item):
                message_text = message_text + item
                next_line = items.__next__()

                if next_line == None:
                    # print(message_text)
                    # print('\end of worship schedule text')
                    write_message_file(message_text, filelist.WorshipScheduleFilename)
                    item = next_line

                    break
                else:
                    item = next_line

            item = next_line  # -- get the next item

        else:
            item = items.__next__()  # --- skip unrecognized line

    if len(status_message) == 0:  # --- no valid message received
        status_message.append('\nUnrecognized message received')

    return status_message
    # --- end Parse the incoming Discord message


def convert_embed(var):
    """
    TODO: document this function
    :param var:
    :return:
    """
    return discord.Embed(description=var)


def status_embed(description, message):
    """
    TODO: Document this function
    :param message:
    :param description:
    :return:
    """
    embed = discord.Embed(color=0x2ECC71, description=description + " was successfully received!")
    embed.add_field(name="Time received:",
                    value=message.created_at.strftime("%b %d %Y %H:%M:%S"),
                    inline=True)
    embed.add_field(name="User:",
                    value=message.author,
                    inline=True)
    return embed
