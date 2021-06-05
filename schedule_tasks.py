#!/usr/bin/env python3
import os
import threading
import time

import schedule

from getdatetime import firstSunday


# --- https://schedule.readthedocs.io/en/stable/
# --- Schedule OpenSong file cleanup
def scheduled_task(scheduled_time='21:33'):
    import threading

    # Every Sunday at 11:00 am cleanup is called
    # schedule.every().sunday.at("11:00").do(cleanup)
    print("ID of process running on 1st thread: {}".format(threading.current_thread().name))
    schedule.every().thursday.at(scheduled_time).do(firstSunday)

    # Loop so that the scheduling task
    # keeps on running all time.

    while True:
        # Checks whether a scheduled task is pending to run or not
        schedule.run_pending()
        time.sleep(10)


# --- end run_scheduled_task

# --- launch the Discord Bot
def run_Discord_Bot():
    import mydiscord

    print("ID of process running Discord Bot: {}".format(threading.current_thread().name))
    mydiscord.read_discord()


# --- end of Discord thread

def main():
    # --- single threaded scheduled task

    # --- run the scheduled clean up tasks every Sunday at 11:000
    print('\nStart Scheduled tasks!')
    # print ID of current process
    print("ID of process running main program: {}".format(os.getpid()))
    print("Main thread name: {}".format(threading.current_thread().name))

    # scheduled_task(scheduled_time='21:10')

    # --- create threads
    t1 = threading.Thread(target=scheduled_task, name='calendar')
    # t2 = threading.Thread(target=run_Discord_Bot, name='discord')

    # starting threads
    t1.start()
    # t2.start()
    run_Discord_Bot()

    # wait until all threads finish
    t1.join()
    # t2.join()


# --- End of function main()

# ------------ Call the Main function to launch the process
if __name__ == "__main__":
    main()
