# SearchSuggestion

This program uses Redis database.
Before using, you have to start redis server
by typing `redis-server` prompt in terminal.


Run `dump_searchlog.py` to make a log file.

Run `create_search_suggestion.py` to make suggestions from the log file.

Use `get_search_suggestion.return_suggestion` to get suggestions for a query.

Use `get_search_suggestion.suggestion_dict` to get all suggestions as a dictionary.


##Using API
To start server type `uvicorn main:app --reload`
in the terminal. Now you can get query suggestion
in the `http://127.0.0.1:8000/query/{query}`.

For example to get suggestions of 'Apple', go to 
`http://127.0.0.1:8000/query/apple`.
