#--- routine to unit test independent functions
        
def main():
    import passagelookup
    import readworshipschedule
    import opensong
    import mydiscord

    #---    test missings songs; why files are being writtent to the wrong directory
    status_message = opensong.cleanup()
    print(status_message)
    return()

    status_message = mydiscord.parsemessage()
    print(status_message)
    return()

    opensong.assembleset()
    return()

    #---    test the multi-part passage parser
    readworshipschedule.readWS()
    return()

    scripture_ref = 'Hebrews 13:22; 1:1–2:4'
    status_message = passagelookup.build_scripture_text(scripture_ref)

    print('\nCurrent Status is')
    for verse in status_message:
        print(verse)

    # ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
    #
if __name__ == "__main__":
    main()
# ======================================================================================