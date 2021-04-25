#---- start dropbox api call
def dropboxsync():
    import dropbox
    import os

    print(os.environ['DROPBOX_ACCESS_TOKEN'])

    DROPBOX_ACCESS_TOKEN = os.environ['DROPBOX_ACCESS_TOKEN']        #--- retrieve token from environment variable

    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)      #--- instantiate a Dropbox token
    dbx.users_get_current_account()

    print('\nDropbox folder list\n')
    for entry in dbx.files_list_folder('').entries:
        print(entry.name)
 
    #print('\nPrint OS.GET Environment variables:', os.getenv('MY_ACCESS_TOKEN'))

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