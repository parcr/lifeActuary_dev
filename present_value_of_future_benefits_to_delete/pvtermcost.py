__author__ = "PedroCR"

import numpy as np
import age


class PVTermCost:
    def __init__(self, date_of_valuation, date_of_birth,
                 date_of_entry, age_of_term_cost, multi_table=None, decrement=None, i=None,
                 age_first_instalment=None, age_last_instalment=None, age_first_payment=None):
        '''
        Creates an instance of a Present Value of a Term Cost object. This object will allow us to get an hold
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
        self.waiting = None

    # def __str__(self):
    #    return '{0}({1})'.format(self.__class__.__name__, 'pcr')

    def __repr__(self) -> str:
        return '{0}({1})'.format(self.__class__.__name__, self.__dict__)

    def __create_dates_ages(self):
        '''
        Creates all dates and ages from y to the age of the first payment
        '''
        # careful when counting years because of the actuarial ages
        dates_ages_past = [
            (age.Age(date1=self.date_of_valuation,
                     date2=self.date_of_valuation).date_inc_years(-j).date2.year,
             self.x - j)
            for j in range(self.past_time_service_years + 1)]

        dates_ages_future = [
            (age.Age(date1=self.date_of_valuation,
                     date2=self.date_of_valuation).date_inc_years(j).date2.year,
             self.x + j)
            for j in range(1, self.future_time_service_years + self.waiting + 1)]
        self.dates_ages = dates_ages_past[::-1] + dates_ages_future

    def __create_dates_ages_w(self):
        '''
        Creates all dates and ages from y to the largest w, expectedly the mortality table's w.
        '''
        # careful when counting years because of the actuarial ages
        self.__create_dates_ages()
        max_w = [t[1].w for t in self.multi_table.unidecrement_tables.items()]
        max_w = max(max_w)
        dates_ages_future = [
            (age.Age(date1=self.date_of_valuation,
                     date2=self.date_of_valuation).date_inc_years(j).date2.year,
             self.x + j)
            for j in range(self.future_time_service_years + self.waiting + 1, max_w - self.x + 1)]
        self.dates_ages_w = self.dates_ages + dates_ages_future

    def set_default_waiting_periods(self):
        self.age_first_instalment = self.y
        self.age_last_instalment = self.age_of_term_cost - 1
        self.age_first_payment = self.age_of_term_cost
        self.waiting = self.age_first_payment - self.age_of_term_cost
        self.__create_dates_ages()
        self.__create_dates_ages_w()

    def prob_survival(self, x):
        '''
        We compute the probability of survival from today (x) until age x, used to project liabilities, considering that
        the decrement occurred, that is, considering that (x) will enter the state defined by the decrement.
        :param x: age of (x)
        :return: The probability of survival considering all the decrements
        '''
        if x <= self.x: return 1
        if x < self.age_of_term_cost:
            tpx_T = self.multi_table.net_table.tpx(self.x, t=x - self.x, method='udd')
        else:
            bool_decrement = bool(self.decrement)
            tpx_T = self.multi_table.net_table.tpx(self.x, t=self.age_of_term_cost - self.x - bool_decrement,
                                                   method='udd') * \
                    self.multi_table.unidecrement_tables['mortality'].tpx(self.age_of_term_cost,
                                                                          t=x - self.age_of_term_cost, method='udd')
        return tpx_T

    def pvftc(self, x):
        '''
        Computes the Present Value of a Future Term Cost, that will allow us to use for all amortization schemes
        :param x: the age fo life (x). We consider that (x) is alive and if the decrement happens, it will be moved to
        to the other state. Hence, if there is a wanting period between the decrement occurrence and the first payment
        (x) should already be placed in the state corresponding to the decrement.
        For instance, if the decrement is disability, immediately after the decrement, (x) is moved to the state of
        disable and there is where the waiting period happens, if any.
        There are states where the decrement happens just due to survival up to that age, for instance, retirement.
        :return: The Present Value of Future Benefits
        '''
        if x < self.y: return 0  # no liability before entry age
        if self.decrement:
            q_d_x = self.multi_table.multidecrement_tables[self.decrement].tqx(self.age_of_term_cost - 1, t=1,
                                                                               method='udd')
        else:
            q_d_x = 1
        if x >= self.age_first_payment: return q_d_x  # full amortization
        if self.y <= x < self.age_of_term_cost:
            if self.decrement:
                tpx_T = self.multi_table.net_table.tpx(x, t=self.age_of_term_cost - x - 1, method='udd')
            else:
                tpx_T = self.multi_table.net_table.tpx(x, t=self.age_of_term_cost - x, method='udd')
            pvft = tpx_T * q_d_x * np.power(self.v, self.age_of_term_cost - x)
            if self.waiting > 0:
                tpx = self.multi_table.unidecrement_tables['mortality'].tpx(x=self.age_of_term_cost, t=self.waiting,
                                                                            method='udd')
                deferment = tpx * np.power(self.v, self.waiting)
                pvft *= deferment
        else:  # no more instalments but still compounding until the first payment
            waiting = self.age_first_payment - x
            tpx = self.multi_table.unidecrement_tables['mortality'].tpx(x, t=waiting, method='udd')
            deferment = np.power(self.v, waiting)
            pvft = q_d_x * tpx * deferment
        return pvft

    def pvtc_x(self):
        return self.pvftc(self.x)

    def vec_pvtc_y_first_payment(self):
        return [x[0] for x in self.dates_ages], \
               [x[1] for x in self.dates_ages], \
               [self.pvftc(x=x[1]) for x in self.dates_ages]

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
        if self.age_first_instalment < x <= self.age_last_instalment:
            return x - self.age_first_instalment
        if x > self.age_last_instalment:
            return self.age_last_instalment + 1 - self.age_first_instalment
        return 0

    def fts_nc(self, x):
        '''
        computes future time service at age x for the normal contributions, that is the instalments
        '''
        return (self.age_last_instalment + 1 - self.age_first_instalment) - self.pts_nc(x)

    def tts_nc(self):
        '''
        computes total time service for the normal contributions, that is the instalments
        '''
        return self.age_last_instalment + 1 - self.age_first_instalment

    '''
    Projecting the term cost
    '''

    def pvtc_proj(self, x):
        return self.pvftc(x) * self.prob_survival(x)

    def vec_pvtc_y_w_proj(self):
        '''
        Computes the projected Present Value for a specific term cost
        :return:
        '''
        return [x[0] for x in self.dates_ages_w], \
               [x[1] for x in self.dates_ages_w], \
               [self.pvtc_proj(x=x[1]) for x in self.dates_ages_w]

    '''
    With age x fixed summing up all the liabilities for this decrement 
    '''

    def vec_pvfb(self, x, age_term_cost_init, age_term_cost_final,
                 dif_age_last_instalment=1, dif_age_first_payment=0):
        '''
        Computes at age x, the Present value of each of the past and future terms costs relative to the decrement
        :param x:
        :param age_term_cost_init:
        :param age_term_cost_final:
        :param dif_age_last_instalment:
        :param dif_age_first_payment:
        :return:
        '''
        ages_term_cost = list(range(age_term_cost_init, age_term_cost_final + 1))
        lst_pvtc = []
        sum_pvftc = 0
        for year_i, year in enumerate(self.dates_ages_w):
            is_zero = self.dates_ages_w[year_i][1] not in ages_term_cost
            pvtc = 0
            if not is_zero:
                atc = self.dates_ages_w[year_i][1]
                self.age_of_term_cost = atc
                self.age_last_instalment = atc - dif_age_last_instalment
                self.age_first_payment = atc + dif_age_first_payment
                pvtc = self.pvftc(x)
            if x < self.dates_ages_w[year_i][1]:
                sum_pvftc += pvtc
            lst_pvtc.append(self.dates_ages_w[year_i] + (pvtc,))
        info_pvftc = (self.age_date_of_valuation.date2.year + (x - self.x), x, sum_pvftc)
        dic_pvtc = {'pvtc_per_year': lst_pvtc, 'sum_pvftc': info_pvftc}
        return dic_pvtc

    def vec_pvfb_x(self, age_term_cost_init, age_term_cost_final,
                   dif_age_last_instalment=1, dif_age_first_payment=0):
        '''
        Computes valuation date, the Present value of each of the future terms costs relative to the decrement
        :param age_term_cost_init:
        :param age_term_cost_final:
        :param dif_age_last_instalment:
        :param dif_age_first_payment:
        :return:
        '''
        return self.vec_pvfb(self.x, age_term_cost_init, age_term_cost_final,
                             dif_age_last_instalment, dif_age_first_payment)

    '''
    With age x fixed summing up all the projected liabilities for this decrement 
    '''

    def vec_pvfb_y_w_proj(self, age_term_cost_init, age_term_cost_final,
                          dif_age_last_instalment=1, dif_age_first_payment=0):
        ages_term_cost = list(range(age_term_cost_init, age_term_cost_final + 1))
        vec_pvtc_y_w_proj = np.zeros(len(self.dates_ages_w))
        for year_i, year in enumerate(self.dates_ages_w):
            is_zero = self.dates_ages_w[year_i][1] not in ages_term_cost
            if not is_zero:
                atc = self.dates_ages_w[year_i][1]
                self.age_of_term_cost = atc
                self.age_last_instalment = atc - dif_age_last_instalment
                self.age_first_payment = atc + dif_age_first_payment
                vec_pvtc_y_w_proj += np.array(self.vec_pvtc_y_w_proj()[2])
        lst_pvfb = [(y[0], y[1], vec_pvtc_y_w_proj[y[1] - self.y]) for y
                    in self.dates_ages_w]
        info_pvfb = ((self.age_date_of_valuation.date2.year, self.x, vec_pvtc_y_w_proj[self.x - self.y]))
        dic_pvtc = {'pvfb_per_year': lst_pvfb, 'sum_pvfb': info_pvfb}
        return dic_pvtc
