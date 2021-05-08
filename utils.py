# Utility functions


# This function will check to see the song(s) passed as a list are valid.
import discord


def parse_songs_from_file(worship_schedule):
    with open(worship_schedule) as file:
        worship_text = file.readlines()
    # Find the line with songs in the array. Assume everything after is a song per line.
    formatted_song_list = []

    for index, song in enumerate(worship_text):
        # Build a list of elements after "Songs" is found.
        if index > worship_text.index('Songs\n'):
            stripped_song = song.split("-")
            stripped_song = stripped_song[0].strip("* ")
            formatted_song_list.append(stripped_song)
    return formatted_song_list


# Takes in a list of songs.
def validate_songs(SongList):
    import maintainsong
    for song in SongList:
        if (maintainsong.displaysong(song)) == "Song Not Found":
            possible_matches = maintainsong.search_songs(song)
            # Build embed object
            embed_data = discord.Embed(title="\'Song " + song + " not found.\'", color=0xe74c3c,
                                       description="Here are some suggestions of similar songs:")

            for match in possible_matches:
                embed_data.add_field(name=match, value=possible_matches[match], inline=False)

            return embed_data
        else:
            embed_data = discord.Embed(title="All Songs are Valid!")
            return embed_data
