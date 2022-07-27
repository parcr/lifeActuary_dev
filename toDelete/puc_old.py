__author__ = "PedroCR"

import numpy as np
from essential_life import age


def default_waiting_periods(date_of_entry, date_of_term_cost):
    waiting_first_instalment = 0
    waiting_last_instalment = age.Age(date1=date_of_entry, date2=date_of_term_cost).age_act() - 1
    waiting_first_payment = 0
    return waiting_first_instalment, waiting_last_instalment, waiting_first_payment


class PUC:
    def __init__(self, date_of_valuation, date_of_birth,
                 date_of_entry, date_of_term_cost, multi_table=None, decrement=None, i=None,
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
        :param waiting_first_instalment: how many periods we wait, after entry age, until the first instalment to
        start amortizing the term cost
        :param waiting_last_instalment: how many periods we wait, after entry age, until the last instalment to finish
        amortizing the term cost
        :param waiting_first_payment: how many periods, after the age of the term cost, until the first payment
        of the term cost
        '''
        self.i = i / 100
        self.v = 1 / (1 + self.i)
        self__date_of_valuation = date_of_valuation
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

        # careful when counting years because of the actuarial ages
        self.ages_dates = [(self.x + j, self.age_x.date2.year + j) for j in range(self.z - self.x + 1)]
        self.ages_dates_all = [(self.ages_dates[0][0] - j, self.ages_dates[0][1] - j) for j in
                               range(1, self.x - self.y)]
        self.ages_dates_all.reverse()
        self.ages_dates_all = self.ages_dates_all + self.ages_dates

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

    def pts(self, x):
        '''
        computes past time service at age x
        '''
        return self.past_time_service_years + (x - self.x)

    def fts(self, x):
        '''
        computes future time service at age x
        '''
        return self.future_time_service_years - (x - self.x)

    def pts_nc(self, x):
        '''
        computes past time service at age x for the normal contributions, that is the instalments
        '''
        if self.y + self.waiting_first_instalment <= x <= self.y + self.waiting_last_instalment:
            return x - (self.y + self.waiting_first_instalment)
        if x > self.y + self.waiting_last_instalment:
            return self.waiting_last_instalment - self.waiting_first_instalment
        return 0

    def fts_nc(self, x):
        '''
        computes future time service at age x for the normal contributions, that is the instalments
        '''
        if self.y + self.waiting_first_instalment <= x <= self.y + self.waiting_last_instalment:
            return (self.y + self.waiting_last_instalment) - x
        return 0

    def tts_nc(self):
        '''
        computes total time service for the normal contributions, that is the instalments
        '''
        return self.waiting_last_instalment - self.waiting_first_instalment

    def pvfb(self, x):
        if x < self.y: return 0  # no liability before entry age
        if x >= self.z + self.waiting_first_payment: return 1  # full amortization
        if self.z <= x < self.z + self.waiting_first_payment:
            # no more instalments but still compounding until the first payment
            return np.power(self.v, self.z + self.waiting_first_payment - x)

        if self.decrement:
            tpx_T = self.multi_table.net_table.npx(x, n=self.z - x - 1, method='udd')
            key_decrement = list(self.multi_table.multidecrement_tables.keys())[self.decrement]
            q_d_x = self.multi_table.multidecrement_tables[key_decrement].nqx(self.z - 1, n=1, method='udd')
        else:
            tpx_T = self.multi_table.net_table.npx(x, n=self.z - x, method='udd')
            q_d_x = 1
        pvft = tpx_T * q_d_x * np.power(self.v, self.z - x)
        if self.waiting_first_payment > 0:
            tpx = self.multi_table.unidecrement_tables['mortality'].npx(x=self.z, n=self.waiting_first_payment,
                                                                        method='udd')
            deferment = tpx * np.power(self.v, self.waiting_first_payment)
            pvft *= deferment
        return pvft

    def pvfb_x(self):
        return self.pvfb(self.x)

    def pvfb_all_ages(self):
        return [x[1] for x in self.ages_dates_all], \
               [x[0] for x in self.ages_dates_all], \
               [self.pvfb(x=x[0]) for x in self.ages_dates_all]

    def al(self, x):
        return self.pvfb(x=x) * self.pts_nc(x) / self.tts_nc()

    def al_x(self):
        return self.al(x=self.x)

    def al_all_ages(self):
        return [x[1] for x in self.ages_dates_all], \
               [x[0] for x in self.ages_dates_all], \
               [self.al(x=x[0]) for x in self.ages_dates_all]

    def nc(self, x):
        if x <= self.y + self.waiting_last_instalment:
            return self.pvfb(x=x) / self.tts_nc()
        return 0

    def nc_x(self):
        return self.nc(x=self.x)

    def nc_all_ages(self):
        return [x[1] for x in self.ages_dates_all], \
               [x[0] for x in self.ages_dates_all], \
               [self.nc(x=x[0]) for x in self.ages_dates_all]
