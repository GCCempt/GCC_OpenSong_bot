# Utility functions that could be re-used elsewhere
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
    Checks the website using the maintainsong.displaysong function to see if the songs are valid.

    :param SongList: A python list of song names to check.
    :param limit: The maximum number of song suggestions to return
    :return: embed data object to be used with discord.py's embed send.
    """
    import maintainsong

    song_error = False
    if SongList == "No songs found.":
        song_error = discord.Embed(title="Songs not found.", color=0xe74c3c,
                                   description="There must be at least one song.")
        return song_error
    for song in SongList:
        display_song = maintainsong.displaysong(song)
        if display_song == "Song Not Found" or "Error" in display_song:
            possible_matches = maintainsong.search_songs(song)
            if possible_matches:
                # Build embed object
                song_error = discord.Embed(title="Song \'" + song + "\' not found.", color=0xe74c3c,
                                           description="Here are some suggestions of similar songs:")

                for index, match in enumerate(possible_matches, 1):
                    song_error.add_field(name=match, value=possible_matches[match], inline=False)
                    if index == limit:
                        break
            else:
                song_error = discord.Embed(title="Song \'" + song + "\' not found.", color=0xe74c3c,
                                           description="We are not able to find any similar song titles.")
        else:
            embed_data = discord.Embed(title="All Songs are Valid!")

    if song_error:
        return song_error
    else:
        return embed_data

#--- ensure proper formatting of scripture references
def parse_passages(input_passages):			#--- input is a scripture reference string
    full_ref_passages = []						#--- list to hold the complete scripture references

    passages = input_passages.replace(',', ';')		#--- standarize ';' as scripture separator
    passages = passages.strip().split(';')	#--- split the string into an array

    #--- get book, chapter, verse
    hold_book_chapter = ''			#-- save the book and chapter reference
    book = ''
    chapter = ''
    scripture = ''
    for p in passages:
        p = p.strip()
        if ' ' in p:				#--- indicates a references includes book; e.g. 'john '
            if ':' in p:				#--- indicates a complete references includes book; e.g. 'john 3:'
                book_chapter, verse = p.split(':', 1)
                book, chapter = book_chapter.split(' ', 1)
                hold_book_chapter = book_chapter.strip()	#--- remove leading and trailing spaces
                passage_ref = hold_book_chapter + ':' + verse
                full_ref_passages.append(passage_ref)
            else:
                passage_ref = hold_book_chapter + ':' + verse   
                full_ref_passages.append(passage_ref)
                book, chapter = hold_book_chapter.split(' ', 1)
        else:
            if ':' in p:    #--- no book; just chapter and verse(s), e.g. 5:1-3
                passage_ref = book + ' ' + p
                full_ref_passages.append(passage_ref)
                book_chapter, ref = passage_ref.split(':', 1)
                hold_book_chapter = str(book_chapter) + ':'

            else:
                verse = p
                passage_ref = hold_book_chapter + ':' + verse
                full_ref_passages.append(passage_ref)       
                book_chapter, ref = passage_ref.split(':', 1)
                #hold_book_chapter = str(book_chapter) + ':'
    return(full_ref_passages)