#!/usr/bin/env python3
# --- program to launch the Discord OpenSong Processing
import os
import threading
import time

import schedule

import mydiscord
from monitorfiles import cleanup


# --- https://schedule.readthedocs.io/en/stable/
# --- Schedule OpenSong file cleanup
def scheduled_task(scheduled_time='13:30'):  # -schedule weekly file cleanup

    # Every Sunday at 13:30 am cleanup is called
    # schedule.every().sunday.at("11:00").do(cleanup)
    print("ID of process running on 1st thread: {}".format(threading.current_thread().name))
    schedule.every().sunday.at(scheduled_time).do(cleanup)

    # Loop so that the scheduling task keeps on running all time.

    while True:
        # Checks whether a scheduled task is pending to run or not
        schedule.run_pending()
        time.sleep(10)


# --- end run_scheduled_task


def main():
    print('\nStart OpenSong Scheduled tasks!')
    # print ID of current process
    print("ID of process running main program: {}".format(os.getpid()))
    print("Main thread name: {}".format(threading.current_thread().name))

    # --- create thread for cleanup process
    t1 = threading.Thread(target=scheduled_task, name='cleanup')

    # starting threads
    t1.start()

    # ---  start the discord Bot
    print("ID of process running Discord Bot: {}".format(threading.current_thread().name))
    mydiscord.read_discord()

    # wait until all threads finish
    t1.join()


# --- End of function main()

# ------------ Call the Main function to launch the process
if __name__ == "__main__":
    main()
