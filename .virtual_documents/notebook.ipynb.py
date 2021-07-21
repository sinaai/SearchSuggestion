from get_search_suggestion import return_suggestion

# all suggestions of 'سلام'
return_suggestion('سلام')


# all suggestions of 'سلام' that repeated at least 2 times
return_suggestion('سلام', method='n-repeated', n=2)


# 4 most repeated suggestions of 'سلام' 
return_suggestion('سلام', method='n-best', n=4)



