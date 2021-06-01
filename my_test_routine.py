
#--- routine to unit test independent functions
def main():
    import processAffirmationOfFaith

    print('\nMy Test Routine - Start Test!\n')
    status_message = processAffirmationOfFaith.read_affirmation_of_faith()
    print(status_message)

    for message in status_message:
        print(message)
    return()


    # ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
    #
if __name__ == "__main__":
    main()
# ======================================================================================