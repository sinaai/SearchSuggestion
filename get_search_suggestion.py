import pickle
import redis


def return_suggestion(query,
                      redis_host='localhost',
                      redis_port=6379,
                      redis_db=9):
    r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
    read_dict = r.get('suggestions')
    suggestions = pickle.loads(read_dict)
    try:
        suggestion = suggestions[query]
    except KeyError:
        suggestion = 'I don\'t have any suggestion!'
    return suggestion


def suggestion_dict(host='localhost', port=6379, db=9):
    r = redis.Redis(host, port, db)
    read_dict = r.get('suggestions')
    suggestion = pickle.loads(read_dict)
    return suggestion
