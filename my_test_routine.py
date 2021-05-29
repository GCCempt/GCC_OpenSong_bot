
#--- routine to unit test independent functions
def main():
    import process_announcements
    #import utils
    #import readworshipschedule

    print('\nMy Test Routine - Start Test!\n')
    status_message = process_announcements.extract_announcement()
    print(status_message)

    return()


    # ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
    #
if __name__ == "__main__":
    main()
# ======================================================================================