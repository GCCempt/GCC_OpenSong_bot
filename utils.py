# Utility functions that could be re-used elsewhere
import logging
from abc import ABC
from html.parser import HTMLParser
from urllib import parse, request
import re

import discord


def parse_songs_from_file(worship_schedule):
    """
    Parses the worshipSchedule.txt and creates a python list of the song names.

    :param worship_schedule: The filename of worship schedule
    :return: python list of song names.
    """

    with open(worship_schedule) as file:
        worship_text = file.readlines()
    # Find the line with songs in the array. Assume everything after is a song per line.
    formatted_song_list = []

    try:
        worship_text.index('Songs\n')
    except ValueError as error:

        return 'No songs found.'
    for index, song in enumerate(worship_text):
        # Build a list of elements after "Songs" is found.
        if "Hymn" in song:
            stripped_song = song.split("-")
            stripped_song = stripped_song[0].strip("Hymn: ")
            formatted_song_list.append(stripped_song)
        if index > worship_text.index('Songs\n'):
            stripped_song = song.split("-")
            stripped_song = stripped_song[0].strip("* ")
            formatted_song_list.append(stripped_song)

    return formatted_song_list


# Takes in a list of songs.
def validate_songs(SongList, limit):
    """
    Performs a case-insensitive check on the given dictionary to find matching
    if the passed songs have any matching keys in the dict.

    :param SongList: A python list of song names to check.
    :param limit: The maximum number of song suggestions to return
    :return: dict with 2 keys; embed data objects to be used with discord.py's embed send and
    a success/fail message. You must iterate through the embed dict to send all the messages.
    """
    url_to_search = 'http://gccpraise.com/opensongv2/xml/'
    invalid_songs = []
    source_data = generate_link_dict(url_to_search)
    embed_messages = {}
    # convert all dictionary keys to lowercase.
    source_data = {k.lower(): v for k, v in source_data.items()}
    # find an exact match within the dictionary.
    status = "invalid songs found."
    for song in SongList:

        if source_data.get(song.lower()) is None:
            invalid_songs.append(song)

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
        status = "All songs are Valid!"

    return_dict = {
        "embed": embed_messages,
        "status": status
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
    with open(song_file) as file:
        file_text = file.readlines()
        file.close()

    for index, line in enumerate(file_text):
        for song in song_list:
            if song.lower() in line.lower():
                file_text[index] = re.sub(song, song, file_text[index])
                logging.info("Updating the song-case of " + song)
    with open(song_file, 'w') as file:
        file.writelines(file_text)
        file.close()

    return None
