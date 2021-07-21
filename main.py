from fastapi import FastAPI
from get_search_suggestion import return_suggestion

app = FastAPI()


@app.get("/")
def read_root():
    return "Search Suggestion App"


@app.get("/query/{query}")
def read_item(query: str):
    return return_suggestion(query, method='all')


@app.get("/repeated/{n}/{query}")
def read_item(query: str, n: int):
    return return_suggestion(query, method='n-repeated', n=n)


@app.get("/best/{n}/{query}")
def read_item(query: str, n: int):
    return return_suggestion(query, method='n-best', n=n)
