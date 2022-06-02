__author__ = "PedroCR"

from present_value_of_future_benefits.pvtermcost import PVTermCost
import numpy as np


class PUC(PVTermCost):
    def __init__(self, date_of_valuation, date_of_birth,
                 date_of_entry, age_of_term_cost, multi_table=None, decrement=None, i=None,
                 age_first_instalment=None, age_last_instalment=None, age_first_payment=None):
        PVTermCost.__init__(self, date_of_valuation, date_of_birth,
                            date_of_entry, age_of_term_cost, multi_table, decrement, i,
                            age_first_instalment, age_last_instalment, age_first_payment)

    def al(self, x):
        if x > self.age_first_instalment:
            return self.pvftc(x=x) * self.pts_nc(x) / self.tts_nc()
        return 0

    def al_x(self):
        return self.al(x=self.x)

    def al_all_ages(self):
        return [x[0] for x in self.dates_ages], \
               [x[1] for x in self.dates_ages], \
               [self.al(x=x[1]) for x in self.dates_ages]

    def nc(self, x):
        if self.age_first_instalment <= x <= self.age_last_instalment:
            return self.pvftc(x=x) / self.tts_nc()
        return 0

    def nc_x(self):
        return self.nc(x=self.x)

    def nc_all_ages(self):
        return [x[0] for x in self.dates_ages], \
               [x[1] for x in self.dates_ages], \
               [self.nc(x=x[1]) for x in self.dates_ages]

    '''
    Testing if the method allows for a correct and full amortization
    '''

    def test(self):  # todo: pass control to log when there is an error
        '''
        Confirms that this is a valid amortization scheme
        :return: sum of the present values of the instalments, difference between the liability and the sum
        of the present values of the instalments and a boolean to check if the difference is smaller than 1e-16
        '''
        all_nc = self.nc_all_ages()
        discount_nc_y = [
            nc * self.multi_table.net_table.npx(self.y, n=nc_i, method='udd') * np.power(self.v, nc_i)
            for nc_i, nc in enumerate(all_nc[2])]
        sum_discount_nc_y = sum(discount_nc_y)
        pvfb_y = self.pvftc(self.y)
        abs_dif = pvfb_y - sum_discount_nc_y
        return sum_discount_nc_y, abs_dif, abs(abs_dif) < 1e-16

    '''
    Projections
    '''

    def al_proj(self, x):
        return self.al(x) * self.prob_survival(x)

    def al_y_w_proj(self):
        return [x[0] for x in self.dates_ages_w], \
               [x[1] for x in self.dates_ages_w], \
               [self.al_proj(x=x[1]) for x in self.dates_ages_w]

    def nc_proj(self, x):
        return self.nc(x) * self.prob_survival(x)

    def nc_y_w_proj(self):
        return [x[0] for x in self.dates_ages_w], \
               [x[1] for x in self.dates_ages_w], \
               [self.nc_proj(x=x[1]) for x in self.dates_ages_w]
