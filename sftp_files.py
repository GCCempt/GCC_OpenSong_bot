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
        'LOCAL_SETS_DIR': 'sets',
        'LOCAL_SONGS_DIR:': 'songs',
        'LOCAL_HOME_DIR': 'bulletin'
    }
#--- end constants definition

#---- start transfer files
def pushfiles(file_type, file_name):
    current_working_directory = os.getcwd()
    print('\nPushFiles() Current Working Directory:', current_working_directory)

    if file_type == 'bulletin':
        remote_file_path = FTPVALUES['REMOTE_BULLETIN_DIR']
        if not 'bulletin' in current_working_directory:
            os.chdir('../bulletin')         #--- switch to the local bulletin directory
    
    elif file_type == 'set':
        remote_file_path = FTPVALUES['REMOTE_SETS_DIR']
        set_path = FTPVALUES['LOCAL_SETS_DIR']

        try:
            os.chdir(set_path)          #-- change to the local sets directory
        except:
            print('\nLocal Sets Directory: {0} does not exit'.format(set_path))
            return()
    
    print('\nStarting File Transfer for:', file_name)

    with pysftp.Connection(host=os.environ['FTP_HOSTNAME'], username=os.environ['FTP_USERNAME'], password=os.environ['FTP_PASSWORD'], cnopts=cnopts) as sftp:
        with sftp.cd(remote_file_path):  #-- switch to the remote directory
            sftp.put(file_name)  # upload file to public/ on remote
            #sftp.get('remote_file')         # get a remote file
    
    print('\nEnd File Transfer for:', remote_file_path, ':', file_name)
#--- end transferfiles

def getfiles():
    #print(os.environ[''])
    print('\nGetFiles() Current Working Directory:', os.getcwd())

    home_path = FTPVALUES['LOCAL_HOME_DIR']
    set_path = FTPVALUES['LOCAL_SETS_DIR']
    try:
        os.chdir(set_path)          #-- change to the local sets directory
    except:
        print('\nDirectory: {0} does not exit'.format(set_path))
        return()
    
    with pysftp.Connection(host=os.environ['FTP_HOSTNAME'], username=os.environ['FTP_USERNAME'], password=os.environ['FTP_PASSWORD'], cnopts=cnopts) as sftp:
        with sftp.cd(FTPVALUES['REMOTE_SETS_DIR']):  #-- switch to the bulletin directory
            sftp.get(FTPVALUES['SET_FILENAME'])  # upload file to public/ on remote
            #sftp.get('remote_file')         # get a remote file
    print('\nEnd Test File Transfer get', FTPVALUES['SET_FILENAME'])

    os.chdir(home_path)          #-- change to the local home directory
#--- end transferfiles

def main():
# ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
#--- below used for standalone testing only
#     import filelist

#    file_type = 'bulletin'
#    pushfiles(file_type, filelist.HTMLBulletinFilename)
    return()

# ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
#
if __name__ == "__main__":
    main()
#
# ======================================================================================