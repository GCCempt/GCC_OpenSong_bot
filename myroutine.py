#--- routine to unit test independent functions
        
def main():
    import passagelookup

    #---    test multi-part scripture ref

    scripture_ref = 'Hebrews 1:1–2:4'
    status_message = passagelookup.build_scripture_text(scripture_ref)

    print('\nScripture Reference Lookup Test', scripture_ref)
    for verse in status_message:
        print(verse)

    # ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
    #
if __name__ == "__main__":
    main()
# ======================================================================================