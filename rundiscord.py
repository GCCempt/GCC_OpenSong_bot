#!/usr/bin/env python3
# --- program to launch the Discord OpenSong Processing
import sys
import startup_validation
import mydiscord
import threading
from schedule_tasks import scheduled_cleanup

def main():
    # --- schedule the weekly file cleanup  on a separate thread
    #t1 = threading.Thread(target=scheduled_cleanup, name='cleanup')

    #---  start the discord Bot
    mydiscord.read_discord()


# --- End of function main()

# ------------ Call the Main function to launch the process
if __name__ == "__main__":
    main()

