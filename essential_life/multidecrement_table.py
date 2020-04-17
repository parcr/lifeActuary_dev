__author__ = "PedroCR"

from essential_life import mortality_table as mt


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
        self.multidecrement_tables = dict()
        self.net_table = None

    def create_udd_multidecrement_table(self):
        lst_w = [t.w for t in self.unidecrement_tables.values()]
        max_w = max(lst_w)
        for k_t, t in self.unidecrement_tables.items():
            copy_tables = self.unidecrement_tables.copy()
            del copy_tables[k_t]
            qx = []
            for i_q, q in enumerate(t.qx):
                factor_to_apply = 1
                for k_t2, t2 in copy_tables.items():
                    factor_to_apply *= (1 - .5 * t2.tqx(i_q, t=1, method='udd'))
                qx.append(q * factor_to_apply)
            # append the first age to the vector of qx
            qx = [0] + qx
            # prepare the table with the probabilities, considering the value of qw=1 or qw=0
            self.multidecrement_tables[k_t] = mt.MortalityTable(mt=qx, last_q=t.last_q)

        # compute the net table, that is the multidecrement qx's and all the remaining fields in a mortality table
        qx = []
        for x in range(max_w + 1):
            q = 0
            for k_t, t in self.multidecrement_tables.items():
                q += t.tqx(x=x, t=1, method='udd')
            qx.append(q)

        # append the first age to the vector of qx
        qx = [0] + qx
        self.net_table = mt.MortalityTable(mt=qx, last_q=1)
