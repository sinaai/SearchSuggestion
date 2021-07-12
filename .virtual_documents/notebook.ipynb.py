from get_search_suggestion import return_suggestion

return_suggestion('سینا')


import redis
import pickle
r = redis.Redis(host='localhost', port=6379, db=9)
read_dict = r.get('suggestions')
suggestion = pickle.loads(read_dict)


suggestion



