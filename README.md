# SearchSuggestion

This program uses Redis database.
Before using, you have to start redis server
by typing `redis-server` prompt in terminal.

### Build suggestions
Run `dump_searchlog.py` to make a log file.

Run `create_search_suggestion.py` to make suggestions from the log file.

Run `auto_build.py` to make log file and build suggestions automatically. 
It will add new suggestions every 12 hours.


### Get suggestions for a query
Use `get_search_suggestion.return_suggestion` to get suggestions for a query.
Use following example.

```python
from get_search_suggestion import return_suggestion

#it returns all of query suggestions in order (most repeated to least repeated)
return_suggestion(query='سلام', method='all') 

#it returns n most repeated query suggestions in order.
return_suggestion(query='سلام', method='n-best', n=n) 

#it returns query suggestions which repeated at least n times.
return_suggestion(query='سلام', method='n-repeated', n=n) 
```


### Using API

To start server type `uvicorn main:app --reload`
in the terminal. Now you can get all query suggestion
in the `http://127.0.0.1:8000/query/{query}`.
For example to get suggestions of 'Apple', go to 
`http://127.0.0.1:8000/query/apple`.

To get n best (most repeated) query suggestions, use `http://127.0.0.1:8000/best/{n}/{query}`.
For example to get 4 best suggestions, go to `http://127.0.0.1:8000/best/4/apple`.

To get query suggestions which repeated at least n times, use `http://127.0.0.1:8000/repeated/{n}/{query}`.
For example to get suggestions which repeated at least 4 times, go to `http://127.0.0.1:8000/repeated/4/apple`.
