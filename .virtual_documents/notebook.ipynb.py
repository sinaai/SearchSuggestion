from get_search_suggestion import return_suggestion

return_suggestion('سینا')


import pickle

suggestion_file='files/search_suggestion.pkl'
pkl_file = open(suggestion_file, "rb")
suggestions = pickle.load(pkl_file)
pkl_file.close()


suggestions



