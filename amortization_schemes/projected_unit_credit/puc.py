__author__ = "PedroCR"

import age


class PUC:
    def __init__(self, date_of_valuation, date_of_birth,
                 date_of_entry, date_of_term_cost, net_table=None, decrement=1, waiting=0):
        '''
        Creates an instance of a Projected Unit Credit amortization scheme
        :param date_of_valuation: date of valuation
        :param date_of_birth: date of birth
        :param date_of_entry: date of entry
        :param date_of_term_cost: date of the first payment of the term cost
        :param net_table: the net table, that is, the multidecrement table used
        :param decrement: the decrement that originates the payment
        :param waiting: how many periods previously to the date of the first payment of the term cost we need to have the
        liability fully funded
        '''
        self.date_of_valuation = date_of_valuation
        self.date_of_birth = date_of_birth
        self.date_of_entry = date_of_entry
        self.date_of_term_cost = date_of_term_cost
        self.net_table = net_table
        self.decrement = decrement
        self.waiting = waiting

        self.past_time_service = age.Age(date1=date_of_entry, date2=date_of_valuation)
        self.future_time_service = age.Age(date1=date_of_valuation, date2=date_of_term_cost)
        self.total_time_service = age.Age(date1=date_of_entry, date2=date_of_term_cost)

        dates_to_consider = list(range(self.past_time_service.date2.year, self.future_time_service.date2.year + 1))
        print(dates_to_consider)
