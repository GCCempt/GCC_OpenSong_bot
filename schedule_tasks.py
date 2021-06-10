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

#--- Scheduled Task Trigger
def task_trigger():
    #--- https://apscheduler.readthedocs.io/en/stable/modules/triggers/cron.html
    from apscheduler.schedulers.background import BackgroundScheduler
    from datetime import datetime
    from time import sleep
    import monitorfiles
    from mydiscord import read_discord

    # The "apscheduler." prefix is hard coded
    scheduler = BackgroundScheduler({
        'apscheduler.executors.default': {
            'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
            'max_workers': '20'
        },
        'apscheduler.executors.processpool': {
            'type': 'processpool',
            'max_workers': '5'
        },
        'apscheduler.job_defaults.coalesce': 'false',
        'apscheduler.job_defaults.max_instances': '3',
    }, daemon=True)

    #--- schedule the automated bulletin check process
    if not scheduler.running:   #-- check if scheduler is currently running
        my_job = scheduler.add_job(monitorfiles.check_for_latest_bulletin, trigger='cron', 
            day_of_week='thu, fri, sat', 
            hour='18',
            minute='15')
        
        scheduler.start() 
    
    scheduler.print_jobs()

    print("Added - {}".format(my_job))

    # ---  start the discord Bot
    print("ID of process running Discord Bot: {}".format(threading.current_thread().name))
    read_discord()

    try:
        while True:
            sleep(10)

    except(KeyboardInterrupt, SystemExit):
        SystemExit

# --- end of Scheduled Task Trigger

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
