__author__ = "PedroCR"


class MultiDecrementTable:
    '''
    Instantiates a multidecrement table with all the needed information, the rates of each decrement and produces
    the net table
    '''

    def __init__(self, dict_table):
        import mortality_table as mt
        if not isinstance(dict_table, dict):
            return
        for t in dict_table:
            if t is not isinstance(t, mt):
                return
        self.unidecrement_table = dict_table
