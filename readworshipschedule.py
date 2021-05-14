# ------------ ReadWS - Read the file containing the Wosrship Schedule extracted from Discord
# --- Definitions for files and directories used in the process
import filelist  # --- definition of list of files and directories used in the proces


def readWS():
    import pickle
    import numpy as np

    # print('\nReadWorshipSchedule - file name: ' + filelist.WorshipScheduleFilename)
    songs = []  # --- array to hold the worship songs and presentation order for each song extracted from Discord into a file
    # print(songs)

    # ----- read the worship schedule file extracted from Discord into a list / array

    textFile = open(filelist.WorshipScheduleFilename, 'r')
    lines = textFile.readlines()

    count = 0
    for line in lines:
        # print('Line{}: {}'.format(count, line.strip()))

        if 'Worship Schedule' in line:
            # print('\nReadWS - Worship Schedule Date:', line)
            ws_date, ws_tag = line.split(' ', 1)
            ws_tag = ws_tag.replace('\n', '')
            songs.append([ws_date, ws_tag])  # --- update list to hold the worship schedule date
            # print('\nSongs start=', songs)

        elif 'Hymn' in line:
            soa = ws_date + line
            # print('\nReadWS - Hymn found:', line, 'Song of Approach=', soa)
            line = line.lstrip('Hymn:')
            # print('\nReadWS line after removing Hymn literal:', line)
            if '#' in line:
                # print('\nReadWS found #')
                line = line.strip()  # --- remove leading and trailing spaces

                ws_hymno, ws_hymn = line.split(' ', 1)  # --- split the line after the 1st space to remove the "#nn "
                # print('\nReadWS - after split; hymno:', ws_hymno, ' hymn:', ws_hymn)
                line = ws_hymn
                parsesong(songs, line)
            else:
                line = line.strip()  # --- remove leading and trailing spaces
                #print('\nLooking for hymn - line=', line)
                # line = ws_hymn

                parsesong(songs, line)

        elif 'Songs' in line:
            for count in range(count, len(lines) - 1):
                count += 1
                # songs.append(lines[count])
                parsesong(songs, lines[count])

            # print('\nReadWS - Praise Songs found:', songs)

        count += 1

    # print('\nEnd of Read Worship Schedule function:\n', songs)

    # --- write the songs 2-dimensional list to a file
    # print('\nSongs=', songs)
    np.savetxt(filelist.SongsFileName, songs,
               fmt='%s')  # --- use numpy module to write 2-dimensional list of songs to file

    # --- read the numpy file to validate contents
    # y = np.loadtxt(filelist.SongsFileName, dtype=np.object)
    # y = y.tolist()
    # y = np.fromfile(filelist.SongsFileName, count=-1, sep=',')

    textFile = open(filelist.SongsFileName, 'r')
    lines = textFile.readlines()
    textFile.close()

    # print('\nSongs File read=',lines)
    # for i in lines:
    #    print(i, end = ' ')
    return ()


# ------------ ParseSong - Split the line into song name and presentation order
def parsesong(songs, line):

    # print('\nParseSong - line: ', line)
    song_name, presentation_order = line.rsplit('-', 1)  # --- split line at 2nd occurrence of '-'

    # print('\nParseSong - url:', url, ' presentation_order:', presentation_order)

    try:
        song_name = song_name.strip('*')  # --- remove leading '*' if found
    except ValueError:
        pass

    song_name = song_name.strip()  # --- remove leading and trailing spaces
    presentation_order = presentation_order.strip().replace(', ', ' ')  # --- remove leading and trailing spaces
    # worship_set.append['Slide group name'(url, presentation_order)
    song_name = song_name + ' - '  # add a deliminter back after the song name for parsing after the file is written

    songs.append(
        [song_name, presentation_order])  # --- update list to hold the worship songs and presentation order for each

    # print('\nParseSong - Song Name:', url, ' Presentation Order:', presentation_order)
    # print(songs)

    return (songs)
