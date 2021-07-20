import pandas as pd
import datetime
import click
import redis


def time_difference(record1, record2):
    time_record1 = datetime.datetime.fromisoformat(record1.time[:-1])
    time_record2 = datetime.datetime.fromisoformat(record2.time[:-1])
    return time_record2 - time_record1


def is_query_edited(record1, record2, time=10):
    if (
            record1.session_id == record2.session_id) and (
            time_difference(record1, record2) < datetime.timedelta(seconds=time)) and (
            time_difference(record1, record2) > datetime.timedelta(seconds=0)) and (
            record1.query_String != record2.query_String
    ):
        return True
    else:
        return False


def create_search_suggestion(search_log_file='files/search_log.jsonl',
                             suggestion_time=10,
                             redis_host='localhost',
                             redis_port=6379,
                             redis_db=9):
    search_log = pd.read_json(search_log_file, lines=True)
    r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
    if r.exists('***checkpoint***'):
        last_checkpoint = int(r.get('***checkpoint***'))
        df = search_log[last_checkpoint:]
    else:
        df = search_log

    for index1, record1 in df.iterrows():
        r.set('***checkpoint***', index1)
        if index1 % 500 == 0:
            print("{:d} out of {:d}".format(index1, search_log.last_valid_index()))
        for index2, record2 in df[df.session_id == record1.session_id].iterrows():
            if is_query_edited(record1, record2, suggestion_time):
                if record1.query_String != '***checkpoint***':
                    r.zincrby(record1.query_String, 1, record2.query_String)

    print("{:d} out of {:d}".format(index1, search_log.last_valid_index()))
    print('Done!')


@click.command()
@click.option('--search-log-file', default='files/search_log.jsonl', type=str)
@click.option('--suggestion-time', default=10, type=int)
@click.option('--redis-host', default='localhost', type=str)
@click.option('--redis-port', default=6379, type=int)
@click.option('--redis-db', default=9, type=int)
def main(search_log_file, suggestion_time, redis_host, redis_port, redis_db):
    create_search_suggestion(search_log_file, suggestion_time, redis_host, redis_port, redis_db)


if __name__ == '__main__':
    main()
