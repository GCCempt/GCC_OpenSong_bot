#!/usr/bin/env python3
import schedule
import time
from monitorfiles import cleanup
from startup_validation import run_test_scripts
import threading
import os

#--- https://schedule.readthedocs.io/en/stable/
# --- Schedule OpenSong file cleanup
def scheduled_cleanup():
    # Every Sunday at 11:00 am cleanup is called
    #schedule.every().sunday.at("11:00").do(cleanup)
    schedule.every().wednesday.at("22:45").do(cleanup)

    # Loop so that the scheduling task
    # keeps on running all time.

    while True:  
        # Checks whether a scheduled task is pending to run or not
        schedule.run_pending()
        time.sleep(1)
#--- end run_scheduled_cleanup


def main():
    # --- run the scheduled clean up tasks every Sunday at 11:000
    print('\nStart Scheduled tasks!')
    # print ID of current process
    print("ID of process running main program: {}".format(os.getpid()))
    print("Main thread name: {}".format(threading.current_thread().name))

    # --- create threads
    t1 = threading.Thread(target=cleanup, name='cleanup')
    t2 = threading.Thread(target=run_test_scripts, name='validation')
    
    # starting threads
    t1.start()
    t2.start()

    # wait until all threads finish
    t1.join()
    t2.join()
# --- End of function main()

# ------------ Call the Main function to launch the process
if __name__ == "__main__":
    main()
