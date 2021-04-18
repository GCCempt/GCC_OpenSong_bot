#!/usr/bin/env python3
#--- program to launch the Discord OpenSong Processing
import mydiscord
import sys

def main():
    for arg in sys.argv[1:]:
        print('Argumeents passed:', arg)
        if 'testing' in arg:
            print('\nStart up argument=', arg)
            mydiscord.read_discord('testing')       #--- start the Discord bot with the "testing" argument
        else:
            continue
    print('\nNormal start - no argument provided')
    mydiscord.read_discord('normal')

#--- End of function main()

#------------ Call the Main function to launch the process
if __name__ == "__main__":
    main()