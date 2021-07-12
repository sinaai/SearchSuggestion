import pandas as pd
import datetime
import pickle
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


def find_suggestions(df, suggestions, search_log, time=10):
    for index1, record1 in df.iterrows():
        suggestions['***checkpoint***'] = index1
        if index1 % 500 == 0:
            print("{:d} out of {:d}".format(index1, search_log.last_valid_index()))
        for index2, record2 in df[df.session_id == record1.session_id].iterrows():
            if is_query_edited(record1, record2, time):
                if (record1.query_String in suggestions) and (record1.query_String != '***checkpoint***'):
                    suggestions[record1.query_String].add(record2.query_String)
                else:
                    suggestions[record1.query_String] = {record2.query_String}
    print("{:d} out of {:d}".format(index1, search_log.last_valid_index()))
    print('Done!')


def create_search_suggestion(search_log_file='files/search_log.jsonl',
                             suggestion_time=10,
                             redis_host='localhost',
                             redis_port=6379,
                             redis_db=9):
    search_log = pd.read_json(search_log_file, lines=True)
    r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
    try:
        read_dict = r.get('suggestions')
        suggestions = pickle.loads(read_dict)
        last_checkpoint = suggestions['***checkpoint***']
        df = search_log[last_checkpoint:]
    except TypeError:
        suggestions = dict()
        df = search_log

    find_suggestions(df, suggestions, search_log, time=suggestion_time)

    p_suggestions = pickle.dumps(suggestions)
    r.set('suggestions', p_suggestions)


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
