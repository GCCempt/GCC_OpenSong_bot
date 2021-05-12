# Utility functions that could be re-used elsewhere
import logging
from abc import ABC
from html.parser import HTMLParser
from urllib import parse, request


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

        if index > worship_text.index('Songs\n'):
            stripped_song = song.split("-")
            stripped_song = stripped_song[0].strip("* ")
            formatted_song_list.append(stripped_song)
    return formatted_song_list


# Takes in a list of songs.
def validate_songs(SongList, limit, source_data):
    """
    Performs a case-insensitive check on the given dictionary to find matching
    if the passed songs have any matching keys in the dict.

    :param source_data: Dictionary of values to check against that contain all the data. (Key-value pair)
    :param SongList: A python list of song names to check.
    :param limit: The maximum number of song suggestions to return
    :return: embed data object to be used with discord.py's embed send.
    """
    invalid_songs = []
    # convert all dictionary keys to lowercase.
    source_data = {k.lower(): v for k, v in source_data.items()}
    for song in SongList:
        if source_data.get(song.lower()) is None:
            invalid_songs.append(song)

    # Start building the discord embed message.



    return embed_data


def generate_link_list(url):
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
