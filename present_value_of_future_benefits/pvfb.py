__author__ = "PedroCR"

import numpy as np
import age


@staticmethod
def default_waiting_periods(date_of_entry, date_of_term_cost):
    waiting_first_instalment = 0
    waiting_last_instalment = age.Age(date1=date_of_entry, date2=date_of_term_cost).age_act() - 1
    waiting_first_payment = 0
    return waiting_first_instalment, waiting_last_instalment, waiting_first_payment


class PVFB:
    def __init__(self, date_of_valuation, date_of_birth,
                 date_of_entry, age_of_term_cost, multi_table=None, decrement=None, i=None,
                 age_first_instalment=None, age_last_instalment=None, age_first_payment=None):
        '''
        Creates an instance of a Present Value Future Benefits object. This object will allow us to get an hold
        in all the information necessary to compute everything we need to valuate actuarial liabilities.
        :param date_of_valuation: date of valuation
        :param date_of_birth: date of birth
        :param date_of_entry: date of entry
        :param age_of_term_cost: date of the first payment of the term cost
        :param multi_table: the net table, that is, the multidecrement table used
        :param decrement: the decrement that originates the payment
        :param i: the technical rate of interest
        :param age_first_instalment: how many periods we wait, after entry age, until the first instalment to
        start amortizing the term cost
        :param age_last_instalment: how many periods we wait, after entry age, until the last instalment to finish
        amortizing the term cost
        :param age_first_payment: how many periods, after the age of the term cost, until the first payment
        of the term cost
        '''

        self.date_of_valuation = date_of_valuation
        self.date_of_birth = date_of_birth
        self.date_of_entry = date_of_entry
        self.age_of_term_cost = age_of_term_cost
        self.multi_table = None
        self.decrement = None
        self.i = i / 100,
        self.age_first_instalment = None
        self.age_last_instalment = None
        self.age_first_payment = None

        self.age_date_of_entry = age.Age(date1=date_of_birth, date2=date_of_entry)
        self.age_date_of_valuation = age.Age(date1=self.date_of_birth, date2=self.date_of_valuation)
        self.x = self.age_date_of_valuation.age_act()
        self.y_ = self.age_date_of_entry.age_f()[3]
        self.y = int(np.ceil(self.y_))

        self.past_time_service_years = self.x - self.y
        self.future_time_service_years = self.age_of_term_cost - self.x
        self.total_time_service_years = self.age_of_term_cost - self.y

        # careful when counting years because of the actuarial ages
        self.ages_dates_past = [
            (self.x - j, age.Age(date1=self.date_of_valuation,
                                 date2=self.date_of_valuation).date_inc_years(-j).date2.year)
            for j in range(self.past_time_service_years + 1)]
        self.ages_dates_future = [
            (self.x +j, age.Age(date1=self.date_of_valuation,
                                 date2=self.date_of_valuation).date_inc_years(j).date2.year)
            for j in range(1, self.future_time_service_years + 1)]

    def set_default_waiting_periods(self):
        self.age_first_instalment = self.y
        self.age_last_instalment = self.age_of_term_cost - 1
        self.age_first_payment = self.age_of_term_cost
