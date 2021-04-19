import os
#--- Definitions for files and directories used in the process
#---          Directories
#bulletinpath = '/root/Dropbox/OpenSongV2/Bulletin'          #--- default directory for writing processing files
#setpath = '/root/Dropbox/OpenSongV2/OpenSong Data/Sets'
#songpath = '/root/Dropbox/OpenSongV2/OpenSong Data/Songs'

bulletinpath = '/var/opt/bulletin'          #--- default directory for writing processing files
setpath = '/mnt/c/Dropbox/OpenSongV2/OpenSong Data/Sets'
songpath = '/mnt/c/Dropbox/OpenSongV2/OpenSong Data/Songs'

os.chdir(bulletinpath)          #--- switch to the default directory for writing files

#----------- Files used for processing
WorshipScheduleFilename = 'worshipschedule.txt'
OldWorshipScheduleFilename = 'old_worshipschedule.txt'   
SermonInfoFilename = 'sermoninfo.txt'
BulletinSermonFilename = 'bulletinsermon.txt'  
AssuranceFilename = 'assurance.txt'
OldAssuranceFilename = 'old_assurance.txt'  
ConfessionFilename = 'confessionofsin.txt'  
OldConfessionFilename = 'old_confessionofsin.txt' 
BulletinFilename = '3-bulletin_name.txt'  
StatusFile = '0-status.txt'
PreviousStatusFile = 'old_0-status.txt'
SetFilename = '2-setname.txt'
CallToWorshipFileName = 'calltoworship.txt'
CurrentStatusFilename = 'currentstatus.txt'
AffirmationFileName = 'affirmation.txt'
ScriptureFileName = 'scripture.txt'
AnnouncementFileName = 'announcement.txt'
SongsFileName = 'songs.txt' 
PDFBulletinFilename = 'bulletin.pdf'
OldPDFBulletinFilename = 'old_bulletin.pdf'
TextPDFBulletinFilename = 'pdf.txt'
TextBulletinFilename = 'bulletin.txt'
OldTextBulletinFilename = 'old_bulletin.txt'
BulletinDateFilename = '1-bulletin_date.txt'
SundaySet = 'NewSundaySet'
HTMLBulletinFilename = 'bulletin.html'
HTMLSermonScriptureFilename = 'sermonscripture.html'
DiscordMessageFilename = 'message.txt'
SongTemplate = 'songtemplate.txt'
NewSongTextFilename = 'newsong.txt'
MessageHistory = 'messagehistory.csv'


#--- End Definitions for files and directories used in the process