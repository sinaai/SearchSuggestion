import pickle


def return_suggestion(query, suggestion_file='files/search_suggestion.pkl'):
    pkl_file = open(suggestion_file, "rb")
    suggestions = pickle.load(pkl_file)
    pkl_file.close()
    try:
        suggestion = suggestions[query]
    except KeyError:
        suggestion = 'I don\'t have any suggestion!'
    return suggestion
