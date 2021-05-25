

#--- routine to unit test independent functions
def main():
    import utils
    import readworshipschedule

    print('\nMy Test Routine - Start Test!\n')
    status_message = readworshipschedule.readWS()
    print(status_message)

    return()


    # ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
    #
if __name__ == "__main__":
    main()
# ======================================================================================