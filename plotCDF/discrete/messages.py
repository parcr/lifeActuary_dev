support_dim = 'we need a 1-dimensional vector.'
needs_array = 'Please, input data, in any form that can be converted to a 1-dimensional array. This includes lists, ' \
              'lists of tuples, tuples, tuples of tuples, tuples of lists and ndarrays. '
needs_1_dim_array = 'We need a 1-dimensional array'
needs_more_than_1 = 'We need a a cardinality greater than 1.'

needs_all_positive = 'We need a vector of probabilities with all values positive.'
needs_lesser_1 = 'We need a vector of probabilities with a sum of positive values equal or lesser than 1.'
needs_same_length = 'We need a support and set of probabilities with the same length.'

needs_same_size = 'Both the support and the set of probabilities must have the same size.'

sum_of_prob = 'The error of the sum of the probabilities exceeds the maximum tolerance allowed for the error. ' \
              'So, you should consider to mark at least one of the tails as incomplete.'

tolerance = 'The tolerance needs to be positive and smaller than 1.'

tails = 'The tails should be True or False. It indicates if the tail is complete, that is, if you are using the ' \
        'minimum and/or maximum mass point of the support, for the left and right tail, respectively.' \
        'By default they are both True.'

is_pmf = 'The is_pmf should be True or False. It indicates if you are using the pmf or the cdf. ' \
         'By default is True.'
