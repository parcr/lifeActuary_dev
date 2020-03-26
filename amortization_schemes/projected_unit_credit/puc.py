__author__ = "PedroCR"

import numpy as np
import age


def default_waiting_periods(date_of_entry, date_of_term_cost):
    waiting_first_instalment = 0
    waiting_last_instalment = age.Age(date1=date_of_entry, date2=date_of_term_cost).age_act() - 1
    waiting_first_payment = 0
    return waiting_first_instalment, waiting_last_instalment, waiting_first_payment


class PUC:
    def __init__(self, date_of_valuation, date_of_birth,
                 date_of_entry, date_of_term_cost, multi_table=None, decrement=1, i=None,
                 waiting_first_instalment=None, waiting_last_instalment=None, waiting_first_payment=None):
        '''
        Creates an instance of a Projected Unit Credit amortization scheme
        :param date_of_valuation: date of valuation
        :param date_of_birth: date of birth
        :param date_of_entry: date of entry
        :param date_of_term_cost: date of the first payment of the term cost
        :param multi_table: the net table, that is, the multidecrement table used
        :param decrement: the decrement that originates the payment
        :param i: the technical rate of interest
        :param waiting_first_instalment: how many periods we wait, after entry age, untilthe first instalment to
        start amortizing the term cost
        :param waiting_last_instalment: how many periods we wait, after entry age, until the last instalment to finish
        amortizing the term cost
        :param waiting_first_payment: how many periods, after the age of the term cost, until the first payment
        of the term cost
        '''
        self.i = i / 100
        self.date_of_valuation = date_of_valuation
        self.date_of_birth = date_of_birth
        self.date_of_entry = date_of_entry
        self.date_of_term_cost = date_of_term_cost
        self.multi_table = multi_table
        self.decrement = decrement
        self.waiting_first_instalment = waiting_first_instalment
        self.waiting_last_instalment = waiting_last_instalment
        self.waiting_first_payment = waiting_first_payment

        self.age_x = age.Age(date1=date_of_birth, date2=date_of_valuation)
        self.age_at_entry = age.Age(date1=date_of_birth, date2=date_of_entry)
        self.past_time_service = age.Age(date1=date_of_entry, date2=date_of_valuation)
        self.future_time_service = age.Age(date1=date_of_valuation, date2=date_of_term_cost)
        self.total_time_service = age.Age(date1=date_of_entry, date2=date_of_term_cost)

        self.y = self.age_at_entry.age_act()
        self.x = self.age_x.age_act()
        self.z = age.Age(date1=date_of_birth, date2=date_of_term_cost).age_act()
        self.past_time_service_years = self.past_time_service.age_act()
        self.future_time_service_years = self.future_time_service.age_act()
        self.total_time_service_years = self.total_time_service.age_act()

        dates_to_consider = list(range(self.past_time_service.date2.year, self.future_time_service.date2.year + 1))
        print(dates_to_consider)

    def set_default_waiting_periods(self):
        '''
        Sets the waiting periods when applying the projected unit credit, that is, with z being the age at the
        end of the year of the term cost.
        The default, being:
        self.waiting_first_instalment = 0
        self.waiting_last_instalment = x-(z-1)
        self.waiting_first_payment = 0

        :return: the default waiting periods when applying the projected unit credit
        '''

        wp = default_waiting_periods(date_of_entry=self.date_of_entry, date_of_term_cost=self.date_of_term_cost)

        # first instalment at age y, the entry age
        self.waiting_first_instalment = wp[0]
        # last instalment at age z-1, the age before the age of the term cost
        self.waiting_last_instalment = wp[1]
        self.waiting_first_payment = wp[2]

    def pvfb(self, x):
        tpx_T = self.multi_table.net_table.tpx(x, t=self.z - x - 1, method='udd')
        key_decrement = list(self.multi_table.multidecrement_tables.keys())[self.decrement]
        q_d_x = self.multi_table.multidecrement_tables[key_decrement].tqx(self.z - 1, t=1, method='udd')
        v = 1 / (1 + self.i)
        return tpx_T * q_d_x * np.power(v, self.z - x) * np.power(v, self.waiting_first_payment)

    def pvfb_x(self):
        return self.pvfb(self.x)
