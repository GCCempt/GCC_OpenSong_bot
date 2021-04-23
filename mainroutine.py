#! python3
import readbulletin             # module to read bulletin file
#import readxmlset               # module to read email and save attachments
import mydiscord                # module to read discord messages
import readworshipschedule      # module to read the worship schedule extracted from Discord
import insertxml                # module to insert Element in XML tree
import addnode                  # modude to add slidegroups to OpenSong set (XML tree)
import downloadbulletin
import extractpdftext           #--- module to extract text from a PDF document
import stringsplit              #--- modulue to split a string by a number followed by a space
import passagelookup            #--- modulue to do API lookup for ESV passage from Crossway
import opensong                 #--- modulue to build the OpenSong set based on bulletin content and Discord postings
import filelist                 #--- definition of list of files and directories used in the proces
import getdatetime              #--- get the current date / time
import monitorfiles             #--- my module to check status of processing
import sys

#--- test writing files under WSL
def writetestfile():
    #textFile = open(BulletinFilename, 'w', encoding='utf-8',errors='ignore')
    textFile = open(testfilename, 'w', encoding='utf-8')
    textFile.write(bulletin)
    textFile.close()
    return
#----- end test write file
 

#--- test the addnode routine
def call_addnode_addscripture():
#----- Add node to XML Set
    inputset_name = 'SampleSet'
    doctree = readxmlset.getxml(inputset_name)                  #--- read the OpenSong set into a xml object
    root = doctree.getroot()

    #doctree = addnode.addsong(doctree, 'Song of Response', 'All in All')   # (slide_group_name, song_name)
    scripture_ref = 'Luke 18:1-8'
    doctree = addnode.addscripture(doctree, 'Sermon', scripture_ref)   # (slide_group_name, scripture reference)

    #root = doctree.getroot()

    print('\nAfter call to Add Node')
    #for slide_group in root.iter('slide_group'):
    #    print(slide_group.tag, slide_group.attrib)

    passagelookup.get_esv_text(scripture_ref, '-')

    return()
#--- end of call_addnode routine

#----- call passagelookup module to retrieve a scripture passage via the API
def call_passagelookup():
#--- retrieve a single passage
    numbers='-'
    passages = 'Romans 1:16'
    scripture = passagelookup.get_esv_text(passages, numbers).replace('[', '').replace(']', '').replace('–', '-').replace('\n\n  ', ':  ')
    
    print(scripture)
    return()
#--- end of call_passagelookup-

#----- call passageSlookup module to retrieve multiple passages via the API
def call_passageslookup():
#--- retrieve a multiple passages
    passages = 'Psalm 24:1–6; John 3:16; Romans 1:16'
    scripture = passagelookup.parse_passages(passages)
    
    print(scripture)
    return()
#--- end of call_createset70-

#----- call stringsplit module to break returned scripture into individual verses
def call_stringsplit():
    text = 'The Parable of the Persistent Widow:  1 And he told them a parable to the effect that they ought always to pray and not lose heart.'
    final = stringsplit.split_on_number(text)
    
    for i in range(0, len(final)):
        print(final[i])
    return()
#--- end of call_stringsplit

#----- call stringsplit module to break string based on newline character
def call_stringsplit_newline():
    text = 'Welcome\nto\nPythonExamples.org'
    final = stringsplit.split_on_newline(text)
    
    for i in range(0, len(final)):
        print(final[i])
    return()
#--- end of call_stringsplit

#----- get underlying operating system information 
def getos():
    import sys

    print(sys.platform)
#--- end of get underlying OS

#----- Print file list constants 
def getfiles():
    import os
    print('\nCurrent Working Directory:', os.getcwd())
    print('\nChanging working directory to parent directory')
    os.chdir(filelist.bulletinpath)
    
    print('\nCurrent Working Directory:', os.getcwd())
    #for root, dirs, files in os.walk("."):
    #    for filename in files:
    #        print(filename)
#--- end of get files

    #----- Add node to XML Set
#--- test the addnode routine
def call_addnode_confession():
    inputset_name = 'SampleSet'
    doctree = readxmlset.getxml(inputset_name)                  #--- read the OpenSong set into a xml object
    root = doctree.getroot()
 
    slide_group_name = 'Call to Worship'
    body_text = opensong.parsecalltoworship()        #--- call the 'parsecalltoworship' routine to separate the text into slides
    
    #addnode.addbodytext(doctree, slide_group_name, body_text) #--- call the addbodytext function
    doctree = addnode.addconfessiontext(doctree, slide_group_name, body_text) #--- call the add body text function

    root = doctree.getroot()

    print('\nAfter call to Add Node')
    #for slide_group in root.iter('slide_group'):
    #    print(slide_group.tag, slide_group.attrib)
#------------ End of function definition

def main():
#--https://realpython.com/python-pass-by-reference/
    print('\nYou are in Main')
    sys.exit(0)
    return()
    return()
#------ Call the subfunctions
#--- test the bulletin parse function
    #mydiscord.parsemessage()
    #sys.exit(0)
    #readbulletin.parsebulletin()
    #readbulletin.selectset()
    #readworshipschedule.readWS()

    #text_string = 'Bulletin Date=Sunday, February 21, 2021  •  11:15 am '
    #monitorfiles.checkbulletinfile()
    #getdatetime.parsedates('**2/28/21 Worship Schedule** ')
    #getdatetime.firstSunday()
    #getdatetime.nextSunday()
    #getdatetime.searchdates('@here here is the confession of sin to be put on screen, 2/28:' )
    #passage = 'Mark 16:9–20'
    #numbers = '-'
    #scripture = passagelookup.get_esv_text(passage, numbers)
    #passagelookup.parse_passages(scripture)
    #print(scripture)
    #monitorfiles.comparefiledates()
    #mydiscord.rerunprocess()

    #body_text = opensong.parsecalltoworship()
    #call_addnode_confession()



    #---- end

    #aof_tag = 'Westminster Confession of  Faith 2.1'
    #readbulletin.aofextract(aof_tag, 23)    
    #return()

    #getfiles()
    #mydiscord.read_discord()                    #--- call the read Discord function to start the Discord Bot
    #mydiscord.post_discord('Test message')
    #downloadbulletin.filewatcher()
    #opensong.buildopensongset()
    #writetestfile()
    #call_createset70()
    #call_convertpdf()

    #readmail.getmessages()

    #opensong.assembleset()

    #readbulletin.parsebulletin()                #--- read the bulletin file into an array
    #listfiles.dirlist()                        #--- call the read Discord function
    #return()
    #readpdfbulletin.webdirlist()
    #return()
    #readmail.readaop()
    #return

    #downloadbulletin.get_bulletin()
    #downloadbulletin.get_date()
    #return()

    
    #readpdfbulletin.pdfminer_extract()
    #return()
    
    #readpdfbulletin.convertpdf()
    #return()
    #readpdfbulletin.extract_text_from_pdf()
    #readpdfbulletin.pdf2text_extract()
    #readpdfbulletin.text_extractor()
    #readpdfbulletin.pypcpdf_extract()
    #readpdfbulletin.convertPDF(bulletinfilepath, OutputtextFilename)

    #return()
    
    #extractpdftext.fitz_extract_text(bulletinfilepath, OutputtextFilename)
    
    #return()

    #extractpdftext.pdf_plumber_extract_text(bulletinfilepath, OutputtextFilename)
    #return()

    #extractpdftext.extract_text(bulletinfilepath, OutputtextFilename)
    #return()
    #---   run the main process
    #createset70.buildset()
    return()
#-- end of function definition routine

if __name__ == "__main__":
    main()