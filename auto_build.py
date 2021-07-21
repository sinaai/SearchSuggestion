import schedule
import time
import os


def job():
    # remove last log file
    log_file = './files/search_log.jsonl'
    if os.path.isfile(log_file):
        os.remove(log_file)

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