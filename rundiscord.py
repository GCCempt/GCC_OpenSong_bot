#!/usr/bin/env python3
# --- program to launch the Discord OpenSong Processing
from schedule_tasks import task_trigger

def main():
    print('\nStart OpenSong Discord Bot!')

    #--- use apscheduler to schedule the background tasks
    task_trigger()    

    # ---  note the Discord Bot is started out of the task_trigger function

# --- End of function main()

# ------------ Call the Main function to launch the process
if __name__ == "__main__":
    main()
