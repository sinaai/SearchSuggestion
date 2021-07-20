import redis


def return_suggestion(query,
                      redis_host='localhost',
                      redis_port=6379,
                      redis_db=9,
                      method='all',
                      n=None):
    r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
    if method == 'all':
        suggestions = r.zrevrange(query, 0, -1)
        suggestions = [x.decode('UTF8') for x in suggestions]
        return suggestions
    if method == 'minimum_repeated':
        suggestions = r.zrevrangebyscore(query, float('inf'), n)
        suggestions = [x.decode('UTF8') for x in suggestions]
        return suggestions
    if method == 'maximum_numbers':
        suggestions = r.zrevrange(query, 0, -1)
        suggestions = [x.decode('UTF8') for x in suggestions]
        return suggestions[:n]
