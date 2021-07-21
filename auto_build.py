import schedule
import time
import os


def job():
    # build a new log file and make suggestions
    os.system('python dump_searchlog.py')
    os.system('python create_search_suggestion.py')
    print('last database update:', time.ctime())


schedule.every(12).hours.do(job)
while True:
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)