__author__ = "PedroCR"

from present_value_of_future_benefits.pvfb import PVFB


class PUC(PVFB):
    def __init__(self, date_of_valuation, date_of_birth,
                 date_of_entry, age_of_term_cost, multi_table=None, decrement=None, i=None,
                 age_first_instalment=None, age_last_instalment=None, age_first_payment=None):
        PVFB.__init__(self, date_of_valuation, date_of_birth,
                      date_of_entry, age_of_term_cost, multi_table, decrement, i,
                      age_first_instalment, age_last_instalment, age_first_payment)

    def al(self, x):
        if x > self.age_first_instalment:
            return self.pvfb(x=x) * self.pts_nc(x) / self.tts_nc()
        return 0

    def al_x(self):
        return self.al(x=self.x)

    def al_all_ages(self):
        return [x[0] for x in self.dates_ages], \
               [x[1] for x in self.dates_ages], \
               [self.al(x=x[1]) for x in self.dates_ages]

    def nc(self, x):
        if self.age_first_instalment <= x <= self.age_last_instalment:
            return self.pvfb(x=x) / self.tts_nc()
        return 0

    def nc_x(self):
        return self.nc(x=self.x)

    def nc_all_ages(self):
        return [x[0] for x in self.dates_ages], \
               [x[1] for x in self.dates_ages], \
               [self.nc(x=x[1]) for x in self.dates_ages]

    '''projections'''

    def al_proj(self, x):
        return self.al(x) * self.prob_survival(x)

    def al_proj_all_ages_proj(self):
        return [x[0] for x in self.dates_ages_w], \
               [x[1] for x in self.dates_ages_w], \
               [self.al_proj(x=x[1]) for x in self.dates_ages_w]

    def nc_proj(self, x):
        return self.nc(x) * self.prob_survival(x)

    def nc_proj_all_ages_proj(self):
        return [x[0] for x in self.dates_ages_w], \
               [x[1] for x in self.dates_ages_w], \
               [self.nc_proj(x=x[1]) for x in self.dates_ages_w]
