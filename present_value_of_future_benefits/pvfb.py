__author__ = "PedroCR"

import numpy as np
import age


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
        self.multi_table = multi_table
        self.decrement = decrement
        self.i = i / 100,
        self.v = 1 / (1 + i / 100)
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

    def __create_dates_ages(self):
        # careful when counting years because of the actuarial ages
        dates_ages_past = [
            (age.Age(date1=self.date_of_valuation,
                     date2=self.date_of_valuation).date_inc_years(-j).date2.year,
             self.x - j)
            for j in range(self.past_time_service_years + 1)]

        waiting = self.age_first_payment - self.age_of_term_cost
        dates_ages_future = [
            (age.Age(date1=self.date_of_valuation,
                     date2=self.date_of_valuation).date_inc_years(j).date2.year,
             self.x + j)
            for j in range(1, self.future_time_service_years + waiting + 1)]
        self.dates_ages = dates_ages_past[::-1] + dates_ages_future

    def set_default_waiting_periods(self):
        self.age_first_instalment = self.y
        self.age_last_instalment = self.age_of_term_cost - 1
        self.age_first_payment = self.age_of_term_cost
        self.__create_dates_ages()

    def pvfb(self, x):
        if x < self.y: return 0  # no liability before entry age
        if x >= self.age_first_payment: return 1  # full amortization
        waiting = self.age_first_payment - self.age_of_term_cost
        if self.y <= x < self.age_of_term_cost:
            if self.decrement:
                tpx_T = self.multi_table.net_table.tpx(x, t=self.age_of_term_cost - x - 1, method='udd')
                q_d_x = self.multi_table.multidecrement_tables[self.decrement].tqx(self.age_of_term_cost - 1, t=1,
                                                                                   method='udd')
            else:
                tpx_T = self.multi_table.net_table.tpx(x, t=self.age_of_term_cost - x, method='udd')
                q_d_x = 1
            pvft = tpx_T * q_d_x * np.power(self.v, self.age_of_term_cost - x)
            if waiting > 0:
                tpx = self.multi_table.unidecrement_tables['mortality'].tpx(x=self.age_of_term_cost, t=waiting,
                                                                            method='udd')
                deferment = tpx * np.power(self.v, waiting)
                pvft *= deferment
        else:  # no more instalments but still compounding until the first payment
            waiting = self.age_first_payment - x
            tpx = self.multi_table.unidecrement_tables['mortality'].tpx(x, t=waiting, method='udd')
            deferment = np.power(self.v, waiting)
            pvft = tpx * deferment
        return pvft

    def pvfb_x(self):
        return self.pvfb(self.x)

    def pvfb_all_ages(self):
        return [x[0] for x in self.dates_ages], \
               [x[1] for x in self.dates_ages], \
               [self.pvfb(x=x[1]) for x in self.dates_ages]
