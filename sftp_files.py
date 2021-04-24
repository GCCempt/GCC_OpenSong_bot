#---- start transfer files
def transferfiles():
    import pysftp

    FTPVALUES = {
        'HOSTNAME': 'moonspell.asoshared.com',
        'USERNAME': 'gccpraise',
        'PASSWORD': 'BaJ5pcl6EpNK',
        'FILENAME': '/bulletin/test.txt',
        'REMOTEDIR': 'bulletin'
    }

    with pysftp.Connection(host=FTPVALUES['HOSTNAME'], username=FTPVALUES['USERNAME'], password=FTPVALUES['PASSWORD']) as sftp:
        with sftp.cd(FTPVALUES['REMOTEDIR']):  # temporarily chdir to public
            sftp.put(FTPVALUES['FILENAME'])  # upload file to public/ on remote
            #sftp.get('remote_file')         # get a remote file
    print('\nEnd Test File Transfer', FTPVALUES['FILENAME'])
#--- end transferfiles

def main():
# ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
#
    transferfiles()
    sys.exit(0)

# ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
#
if __name__ == "__main__":
    main()
#
# ======================================================================================