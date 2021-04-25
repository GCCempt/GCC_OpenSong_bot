#---- start transfer files
def transferfiles():
    import pysftp
    import os

    FTPVALUES = {
        'HOSTNAME': 'moonspell.asoshared.com',
        'USERNAME': 'gccpraise',
        'BULLETIN_FILENAME': 'bulletin/test.txt',
        'REMOTEDIR': '/home/gccpraise/public_html/bulletin'
    }
    #print(os.environ[''])
    with pysftp.Connection(host=FTPVALUES['HOSTNAME'], username=FTPVALUES['USERNAME'], password=os.environ['FTP_PASSWORD']) as sftp:
        with sftp.cd(FTPVALUES['REMOTEDIR']):  # temporarily chdir to public
            sftp.put(FTPVALUES['BULLETIN_FILENAME'])  # upload file to public/ on remote
            #sftp.get('remote_file')         # get a remote file
    print('\nEnd Test File Transfer', FTPVALUES['BULLETIN_FILENAME'])
#--- end transferfiles

def main():
# ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
#
    transferfiles()
    return()

# ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
#
if __name__ == "__main__":
    main()
#
# ======================================================================================