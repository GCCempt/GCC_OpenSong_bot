#---- sync to dropbox using dropbox api
#--- reference: https://www.dropbox.com/developers/documentation/python
def dropboxsync():
    import dropbox
    import os

    #print(os.environ['DROPBOX_ACCESS_TOKEN'])
    current_working_directory = os.getcwd()
    print('\nDropbox Api() Current Working Directory:', current_working_directory)

    file_name ='/2021-05-02 GCCEM Sunday Worship'


    DROPBOX_ACCESS_TOKEN = os.environ['DROPBOX_ACCESS_TOKEN']        #--- retrieve token from environment variable

    #local_file_path = ''        #--- path to local file
    dropbox_sets_path = '/Sets'           #--- path to dropbox Sets folder
    dropbox_songs_path = '/Songs'

    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)      #--- instantiate a Dropbox token
    dbx.users_get_current_account()

    print('\nDropbox folder list\n')
    for entry in dbx.files_list_folder('').entries:
        print(entry.name)

    dropbox_path = '/OpenSongV2/OpenSong Data/Sets/2021-05-02 GCCEM Sunday Worship'
    computer_path = 'sets/2021-05-02 GCCEM Sunday Worship'
    #--- upload the file to Dropbox from the local file
    dbx.files_upload(open(computer_path, "rb").read(), dropbox_path)
    print("[UPLOADED] {}".format(dropbox_path))
    dbx.close()

#--- end dropbox sync

def main():
# ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
#
    dropboxsync()
    return()

# ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
#
if __name__ == "__main__":
    main()
#
# ======================================================================================