import logging

import utils
from utils import generate_random_worship_schedule


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
