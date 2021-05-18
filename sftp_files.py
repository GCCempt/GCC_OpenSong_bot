#--- sftp files to / from the gccpraise website
#--- constants
import pysftp
import os

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

FTPVALUES = {
        'BULLETIN_FILENAME': 'bulletin/test.txt',
        'SET_FILENAME': 'SampleSet-NoGloriaPatriWCommunion',
        'REMOTE_BULLETIN_DIR': '/home/gccpraise/public_html/bulletin',
        'REMOTE_SETS_DIR': '/home/gccpraise/public_html/opensongv2/sets',
        'REMOTE_SONGS_DIR': '/home/gccpraise/public_html/opensongv2/xml',
        'LOCAL_SETS_DIR': 'sets/',
        'LOCAL_SONGS_DIR:': 'songs/',
        'LOCAL_BULLETIN_DIR': 'bulletin/'
    }
#--- end constants definition

#---- start transfer files
def pushfiles(file_type, file_name):
    if file_type == 'bulletin':
        remote_file_path = FTPVALUES['REMOTE_BULLETIN_DIR']
        local_file_name = FTPVALUES['LOCAL_BULLETIN_DIR'] + file_name
    
    elif file_type == 'set':
        remote_file_path = FTPVALUES['REMOTE_SETS_DIR']
        local_file_name = FTPVALUES['LOCAL_SETS_DIR'] + file_name

    print('\nStarting Push File Transfer for:', file_name)

    with pysftp.Connection(host=os.environ['FTP_HOSTNAME'], username=os.environ['FTP_USERNAME'], password=os.environ['FTP_PASSWORD'], cnopts=cnopts) as sftp:
        with sftp.cd(remote_file_path):  #-- switch to the remote directory
            sftp.put(local_file_name)  # upload file to public/ on remote
    
    print('\nEnd Push File Transfer for:', remote_file_path, ':', local_file_name)
#--- end Push transferfiles

def getfiles(file_type, file_name):
    if file_type == 'bulletin':
        remote_file_path = FTPVALUES['REMOTE_BULLETIN_DIR']
        local_file_name = FTPVALUES['LOCAL_BULLETIN_DIR'] + file_name
    
    elif file_type == 'set':
        remote_file_path = FTPVALUES['REMOTE_SETS_DIR']
        local_file_name = FTPVALUES['LOCAL_SETS_DIR'] + file_name

    print('\nStarting Get File Transfer for:', file_name)
    
    with pysftp.Connection(host=os.environ['FTP_HOSTNAME'], username=os.environ['FTP_USERNAME'], password=os.environ['FTP_PASSWORD'], cnopts=cnopts) as sftp:
        with sftp.cd(remote_file_path):  #-- switch to the sets directory
            sftp.get(local_file_name)  # retrieve file from the website
            #sftp.get('remote_file')         # get a remote file
    print('\nEnd Test Get File Transfer', local_file_name)

#--- end transferfiles

def main():
# ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
#--- below used for standalone testing only
#     import filelist

#    file_type = 'bulletin'
#    pushfiles(file_type, filelist.HTMLBulletinFilename)
#    return()

# ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
#
    if __name__ == "__main__":
        main()
#
# ======================================================================================