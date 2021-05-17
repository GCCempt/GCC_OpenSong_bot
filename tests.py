import datetime
import logging
from random import *

import names

import utils


def test_parse_songs_from_file():
    # Create dictionary of songs to use for our test.
    song_dict = utils.generate_link_dict("http://gccpraise.com/opensongv2/xml/")

    # Create a random file to edit.
    hymn_filename = 'parse_hymn_tests.txt'
    generate_random_worship_schedule(hymn_filename)

    # Get a list of the songs in the random file.
    starting_songs = utils.parse_songs_from_file(hymn_filename)
    starting_hymn = starting_songs[0]
    starting_song = starting_songs[1]

    with open(hymn_filename) as f:
        worship_text = f.readlines()

    list_of_songs = list(song_dict.keys())

    # Do initial replacement to prepare for the loop
    worship_text = [sub.replace(starting_hymn, list_of_songs[0]) for sub in worship_text]
    worship_text = [sub.replace(starting_song, list_of_songs[0]) for sub in worship_text]
    previous_song = list_of_songs[0]

    # Try each song - replacing only the hymn.
    logging.debug("***** Performing song validation from parsing. ******")
    for song in song_dict:
        worship_text = [sub.replace(previous_song, song) for sub in worship_text]
        with open(hymn_filename, 'w') as f:
            f.writelines(worship_text)
        previous_song = song
        # File is now updated - test the parsing.
        results = utils.parse_songs_from_file(hymn_filename)
        hymn_result = results[0]
        song_result = results[1]
        expectation = song

        logging.debug(
            "Testing Hymn: --> {result} == {expectation} ".format(result=hymn_result, expectation=expectation))
        assert hymn_result == expectation, "Result: {result} \n Expectation: {expectation}\n".format(result=hymn_result,
                                                                                                     expectation=
                                                                                                     expectation)

        logging.debug(
            "Testing Song: --> {result} == {expectation} ".format(result=hymn_result, expectation=expectation))
        assert song_result == expectation, "Result: {result} \n Expectation: {expectation}\n".format(result=song_result,
                                                                                                     expectation=
                                                                                                     expectation)


def generate_song_name():
    song_dict = utils.generate_link_dict("http://gccpraise.com/opensongv2/xml/")
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
    return None