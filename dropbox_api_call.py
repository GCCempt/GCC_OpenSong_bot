#---- sync to dropbox using dropbox api
#--- reference: https://www.dropbox.com/developers/documentation/python
def dropboxsync(file_type, file_name):
    import dropbox
    import os

    current_working_directory = os.getcwd()
    print('\nDropbox Api() Current Working Directory:', current_working_directory)
    #os.chdir('../')  # -- switch back to the default directory
    #print('\nDropbox Api() print directory listing after switch Working Directory:', current_working_directory)
    print(os.listdir())

    DROPBOX_ACCESS_TOKEN = os.environ['DROPBOX_ACCESS_TOKEN']        #--- retrieve token from environment variable

     #--- set the path to destination dropbox folder
    if file_type == 'set':
        dropbox_path = '/OpenSongV2/OpenSong Data/Sets/' + file_name
        if 'sets' in current_working_directory:
            computer_path = current_working_directory + '/' + file_name
        else:
            os.chdir('sets')        #--- switch to the sets directory
            computer_path = 'sets/' + file_name
    else:
        dropbox_path = '/OpenSongV2/OpenSong Data/Songs/' + file_name
        computer_path = 'songs/' + file_name

    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)      #--- instantiate a Dropbox token
    dbx.users_get_current_account()

    print('\nDropbox folder list\n')
    for entry in dbx.files_list_folder('').entries:
        print(entry.name)

    #--- upload the file to Dropbox from the local file
    dbx.files_upload(open(computer_path, "rb").read(), dropbox_path)
    print("[UPLOADED] {}".format(dropbox_path))
    dbx.close()

#--- end dropbox sync

def main():
# ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
#-- following values are hard_code for testing; commment out for live run
    #file_name ='2021-05-02 GCCEM Sunday Worship'
    #file_type ='set'

    dropboxsync(file_type, file_name)
    return()

# ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
#
if __name__ == "__main__":
    main()
#
# ======================================================================================