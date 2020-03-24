__author__ = "PedroCR"


class MultiDecrementTable:
    '''
    Instantiates a multidecrement table with all the needed information, the rates of each decrement and produces
    the net table
    '''

    def __init__(self, dict_tables):
        if not isinstance(dict_tables, dict):
            return
        for k, v in dict_tables.items():
            if 'MortalityTable' not in str(v.__class__):
                return
        self.unidecrement_tables = dict_tables

    def create_udd_multidecrement_table(self):
        copy_tables = self.unidecrement_tables.copy()
        lst_w = [t.w for t in self.unidecrement_tables.values()]
        max_w = max(lst_w)
        for k_t, t in self.unidecrement_tables.items():
            del copy_tables[k_t]
