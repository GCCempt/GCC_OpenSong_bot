# ---- sync to dropbox using dropbox api
# --- reference: https://www.dropbox.com/developers/documentation/python
def dropboxsync(file_type, file_name):
    import dropbox
    from dropbox.files import WriteMode
    import os

    DROPBOX_ACCESS_TOKEN = os.environ['DROPBOX_ACCESS_TOKEN']  # --- retrieve token from environment variable
    set_path = 'sets/'
    song_path = 'songs/'
    local_computer_path = file_name

    current_working_directory = os.getcwd()
    print('\nDropbox Api() Current Working Directory listing:', current_working_directory, 'input file_name=',
          file_name)

    print(os.listdir())

    # --- set the path to destination dropbox folder
    if file_type == 'set':
        dropbox_path = '/OpenSongV2/OpenSong Data/Sets/' + file_name
        local_computer_path = set_path + file_name
    else:
        dropbox_path = '/OpenSongV2/OpenSong Data/Songs/' + file_name
        local_computer_path = song_path + file_name

    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)  # --- instantiate a Dropbox token
    dbx.users_get_current_account()

    print('\nDropbox folder list\n')
    for entry in dbx.files_list_folder('').entries:
        print(entry.name)

    # --- upload the file to Dropbox from the local file

    dbx.files_upload(open(local_computer_path, "rb").read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)
    print("[UPLOADED] {}".format(dropbox_path))
    dbx.close()


# --- end dropbox sync

def main():
    # ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
    # -- following values are hard_code for testing; commment out for live run
    # file_name ='2021-05-02 GCCEM Sunday Worship'
    # file_type ='set'

    # dropboxsync(file_type, file_name)
    return ()


# ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
#
if __name__ == "__main__":
    main()
#
# ======================================================================================
