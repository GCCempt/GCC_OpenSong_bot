#!/usr/bin/env python3
import schedule
import time
from monitorfiles import cleanup
import startup_validation

#--- https://schedule.readthedocs.io/en/stable/
# --- Schedule OpenSong file cleanup
def scheduled_cleanup():
    # Every Sunday at 11:00 am cleanup is called
    schedule.every().sunday.at("11:00").do(cleanup)

    # Loop so that the scheduling task
    # keeps on running all time.

    while True:  
        # Checks whether a scheduled task is pending to run or not
        schedule.run_pending()
        time.sleep(1)
#--- end run_scheduled_cleanup

# --- TESTING - Schedule start for OpenSong Validation
def start_OpenSong_Validation():
    print('\nSchedule OpenSong Validation')

    startup_validation.run_test_scripts()
    
    return schedule.CancelJob


#--- end run_scheduled_Discord Bot start

def main():
    # --- run the scheduled clean up tasks every Sunday at 11:000
    print('\nSchedule cleanup task')
    scheduled_cleanup()

    
    #--- TESTING - launch the scheduled tasks
    #schedule.every().day.at('11:15').do(start_OpenSong_Validation)

    #while True:
    #    schedule.run_pending()
    #    time.sleep(1)

# --- End of function main()

# ------------ Call the Main function to launch the process
if __name__ == "__main__":
    main()
