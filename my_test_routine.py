#--- routine to schedule tasks
#--- https://apscheduler.readthedocs.io/en/stable/userguide.html
#--- https://github.com/agronholm/apscheduler
#--- https://betterprogramming.pub/introduction-to-apscheduler-86337f3bb4a6

#--- imports
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.events import JobEvent

import logging
import monitorfiles
    
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

#--- Task Schedule
def task_scheduler():
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
    })

# Initialize the rest of the application here, or before the scheduler initialization
    try:
        my_job = scheduler.add_job(monitorfiles.filechecker, 'interval', minutes=1) 

        #my_job.remove()     #--- remove the instance of the scheduled job
    except (KeyboardInterrupt, SystemExit):
        pass
    
    scheduler.start()

    scheduler.print_jobs()
#--- end task schedule routine

#--- Task Trigger
def task_trigger():
    from datetime import datetime
    from time import sleep

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
    })


    if not scheduler.running:   #-- check if scheduler is currently running
        my_job = scheduler.add_job(monitorfiles.check_for_latest_bulletin, trigger='cron', day_of_week='wed', minute='05')
        scheduler.start() 
    
    scheduler.print_jobs()

    print("Added - {}".format(my_job))

    try:
        while True:
            sleep(10)

    except(KeyboardInterrupt, SystemExit):
        SystemExit

#--- end task trigger




#--- main routine to unit test independent functions
def main():
    import downloadbulletin
    from getdatetime import nextSunday

    print('\nMy Test Routine - Start Test!\n')

    task_trigger()

    # ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
    #
if __name__ == "__main__":
    main()
# ======================================================================================