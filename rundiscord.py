#!/usr/bin/env python3
# --- program to launch the Discord OpenSong Processing
import mydiscord
import sys
import test_script


def main():
    for arg in sys.argv[1:]:
        print('Argumeents passed:', arg)
        if 'testing' in arg:
            print('\nStart up argument=', arg)
            mydiscord.read_discord('testing')  # --- start the Discord bot with the "testing" argument
        else:
            continue
    print('\nNormal start - no argument provided')

    #--- call the test / validation script as the first thing before the bot starts
    test_script.run_test_scripts()

    #---  start the discord Bot
    mydiscord.read_discord('normal')

# --- End of function main()

# ------------ Call the Main function to launch the process
if __name__ == "__main__":
    main()

