# write-html.py
import filelist

set_path = 'sets/'
bulletin_path = 'bulletin/'


# --- retrieve the content to be included in the HTML file
def readctw():
    # --- read the call to worship file
    textFile = open(bulletin_path + filelist.CallToWorshipFileName, 'r', encoding='utf-8', errors='ignore')
    status_message = textFile.readlines()  # --- read the first line from the file
    textFile.close()

    ctw = status_message[1]  # --- get the Call To Worship reference

    return (ctw)


# --- end retrieve call to worship

# --- retrieve the Scripture Reading file
def readscripture():
    # --- read the Scripture Reading file
    textFile = open(bulletin_path + filelist.ScriptureFileName, 'r', encoding='utf-8', errors='ignore')
    status_message = textFile.readlines()  # --- read the first line from the file
    textFile.close()

    scripture_text = status_message[1]  # --- get the Call To Worship reference

    return (scripture_text)


# --- end retrieve call to worship

# --- retrieve the songs to be included in the HTML file
def readsongs():
    import readworshipschedule
    # --- get the list of worship songs
    songs = readworshipschedule.readWS()

    soa = songs[1][0]
    sor = songs[4][0]
    sop1 = songs[2][0]
    sop2 = songs[3][0]

    return (soa, sop1, sop2, sor)
# --- end retrieve songs

# --- retrieve the sermon text to be included in the HTML file
def readsermon():
    # --- read the sermon text file
    textFile = open(bulletin_path + filelist.SermonInfoFilename, 'r', encoding='utf-8', errors='ignore')
    status_message = textFile.readlines()  # --- read the file into a list
    textFile.close()

    sermon = status_message[1]  # --- get the sermon text
    return (sermon)


# --- end retrieve sermon

# --- retrieve the assurance of pardon text to be included in the HTML file
def readassurance():
    # --- read the sermon text file
    textFile = open(bulletin_path + filelist.AssuranceFilename, 'r', encoding='utf-8', errors='ignore')
    status_message = textFile.readlines()  # --- read the file into a list
    textFile.close()

    assurance = status_message[1]  # --- get the sermon text
    return (assurance)


# --- end retrieve sermon

# --- retrieve the bulletin date to be included in the HTML file
def readbulletindate():
    # --- read the sermon text file
    textFile = open(bulletin_path + filelist.BulletinDateFilename, 'r', encoding='utf-8', errors='ignore')
    status_message = textFile.readlines()  # --- read the first line from the file
    textFile.close()

    bulletin_date = status_message[0]  # --- get the sermon text
    return (bulletin_date)


# --- end retrieve sermon

# --- main routine
def buildhtmlcontent():
    message = data = """<html>
    <head></head>
    <body><p>Order of Worship for bulletin_date!</p>
    temp
    </body>
    </html>"""
    data = """
        Call To Worship;    ctw_text
        Song of Approach;   soa
        Songs of Praise;    Song1 
        ;                   Song2
        Assurance of Pardon;    assurance_ref
        Scripture Reading;    scripture_text
        Sermon;    sermon_text
        Song of Response;    sor
    """

    data = data.splitlines()
    data = [d.strip() for d in data]
    data = [f"<tr><td>{d}</tr>" for d in data if d.strip() != ""]
    data = "<table border=1>" + "".join(data) + "</table>"
    # display(HTML(data))
    data = data.replace("    ", "")
    data = data.replace(";", "</td><td>")
    # data
    # --- retrieve call to worship
    ctw = readctw()
    data = data.replace('ctw_text', ctw)

    # --- retrieve songs
    soa, sop1, sop2, sor = readsongs()
    data = data.replace('soa', soa)
    data = data.replace('sor', sor)
    data = data.replace('Song1', sop1)
    data = data.replace('Song2', sop2)

    # --- retrieve sermon
    sermon = readsermon()
    data = data.replace('sermon_text', sermon)

    # --- retrieve scripture
    scripture = readscripture()  # --- call the read scripture function
    data = data.replace('scripture_text', scripture)

    # --- retrieve assurance of pardone
    assurance = readassurance()  # --- call the read scripture function
    data = data.replace('assurance_ref', assurance)

    # --- retrieve bulletin date
    bulletin_date = readbulletindate()  # --- call the read bulletin date function
    message = message.replace('bulletin_date', bulletin_date)

    # --- update the HTML text
    message = message.replace('temp', data)

    # --- Write the HTML file
    f = open(bulletin_path + filelist.HTMLBulletinFilename, 'w')
    f.write(message)
    f.close()

    # --- Call the routine to build the HTML file for the sermon text
    buildSermonScriptureContent()


# --- end def buildhtmlcontent():

# --- build html sermon scripture file for the website iframe
def buildSermonScriptureContent():
    import passagelookup
    import stringsplit
    import utils
 
    print('\nStarting BuildSermonScriptureContent')

    # -- retrieve the sermon scripture from the sermon text file
    scripture_ref, sermon_title = utils.extract_sermon_info()  
    if "failed" in scripture_ref:
        return()

    # --- FOR TESTING - OVERRIDE WITH DEFAULT VALUE
    # scripture_ref = 'Galatians 2:1–10; John 3:16'

    verses = passagelookup.build_scripture_text(scripture_ref)  # --- returns a list of verses
    scripture = stringsplit.convertListToString(verses)  # --- convert the list to a string

    message = data = """<html>
    <head></head>
    <body>
        <h1>Sermon Text: reference</h1>
        temp
    </body>
    </html>"""

    # --- update the HTML text
    message = message.replace('reference', scripture_ref)
    message = message.replace('temp', scripture)

    # --- Write the Bulletin Sermon Scripture HTML file
    f = open(bulletin_path + filelist.HTMLSermonScriptureFilename, 'w')
    f.write(message)
    f.close()

# --- end def buildhtmlcontent():
