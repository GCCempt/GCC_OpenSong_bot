#--- routine to unit test independent functions
        
def main():
    import utils
    from monitorfiles import set_cleanup

    status_message = set_cleanup()
    print('\nStatus =', status_message)
    return()


    # ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
    #
if __name__ == "__main__":
    main()
# ======================================================================================