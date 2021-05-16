import datetime
from random import *

import names

import utils


def test_parse_songs_from_file():
    utils.parse_songs_from_file(generate_random_worship_schedule('tests/worshipschedule.txt'))




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
