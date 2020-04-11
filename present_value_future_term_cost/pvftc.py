__author__ = "PedroCR"

import numpy as np
import age


class PVTermCost:
    def __init__(self, date_of_valuation, date_of_birth, date_of_entry,
                 age_of_term_cost, waiting=0,
                 multi_table=None, decrement=None,
                 i=None,
                 age_of_projection=None):
        '''
        Creates an instance of a Present Value of a Term Cost object. This object will allow us to get an hold
        in all the information necessary to compute everything we need to valuate actuarial liabilities.
        :param date_of_valuation: date of valuation
        :param date_of_birth: date of birth
        :param date_of_entry: date of entry
        :param age_of_term_cost: the age at which x accesses the state of the term cost, that is, the age where the
        decrement occurs
        :param waiting: age_of_term_cost+waiting=age_first_payment : how many periods, after the age of the term cost,
        until the first payment of the term cost
        :param multi_table: the net table, that is, the multidecrement table used
        :param decrement: the decrement that originates the payment
        :param i: the technical rate of interest
        :param age_of_projection: The age for each we are projecting the present value of the term cost if x lives to
        age_of_projection
        '''

        self.set_date_of_valuation(date_of_valuation)
        self.set_date_of_birth(date_of_birth)
        self.set_date_of_entry(date_of_entry)
        self.__dates_ages_w = None

        self.set_multi_table(multi_table)
        self.set_decrement(decrement)

        self.set_age_date_of_entry()
        self.set_age_date_of_valuation()

        self.set_y_()
        self.set_y()
        self.set_x()

        # this needs to be recomputed whenever changed
        self.age_of_term_cost = age_of_term_cost
        self.waiting = waiting

        self.i = i / 100,
        self.age_of_projection = age_of_projection
        self.v = 1 / (1 + i / 100)

    @property
    def date_of_valuation(self):
        return self.__date_of_valuation

    def set_date_of_valuation(self, d):
        self.__date_of_valuation = d

    @property
    def date_of_birth(self):
        return self.__date_of_birth

    def set_date_of_birth(self, d):
        self.__date_of_birth = d

    @property
    def date_of_entry(self):
        return self.__date_of_entry

    def set_date_of_entry(self, d):
        self.__date_of_entry = d

    @property
    def multi_table(self):
        return self.__multi_table

    def set_multi_table(self, m):
        self.__multi_table = m

    @property
    def decrement(self):
        return self.__decrement

    def set_decrement(self, d):
        self.__decrement = d

    @property
    def age_date_of_entry(self):
        return self.__age_date_of_entry

    def set_age_date_of_entry(self):
        self.__age_date_of_entry = age.Age(self.__date_of_birth, self.__date_of_entry)

    @property
    def age_date_of_valuation(self):
        return self.__age_date_of_valuation

    def set_age_date_of_valuation(self):
        self.__age_date_of_valuation = age.Age(self.__date_of_birth, self.__date_of_valuation)

    @property
    def y_(self):
        return self.__y_

    def set_y_(self):
        self.__y_ = self.age_date_of_entry.age_f()[3]

    @property
    def y(self):
        return self.__y

    def set_y(self):
        self.__y = int(np.ceil(self.y_))

    @property
    def x(self):
        return self.__x

    def set_x(self):
        self.__x = self.age_date_of_valuation.age_act()

    @property
    def age_of_term_cost(self):
        return self.__age_of_term_cost

    @age_of_term_cost.setter
    def age_of_term_cost(self, atc):
        self.__age_of_term_cost = atc
        self.__past_time_service_years = self.x - self.y
        self.__future_time_service_years = self.age_of_term_cost - self.x
        self.__total_time_service_years = self.age_of_term_cost - self.y
        try:
            self.__age_first_payment = self.age_of_term_cost + self.waiting
        except AttributeError as ae:
            pass

        if self.dates_ages_w is None:
            self.set_dates_ages_w()

    @property
    def waiting(self):
        return self.__waiting

    @waiting.setter
    def waiting(self, w):
        self.__waiting = w
        self.__age_first_payment = self.age_of_term_cost + self.waiting

    @property
    def age_first_payment(self):
        return self.__age_first_payment

    @property
    def past_time_service_years(self):
        return self.__past_time_service_years

    @property
    def future_time_service_years(self):
        return self.__future_time_service_years

    @property
    def total_time_service_years(self):
        return self.__total_time_service_years

    @property
    def dates_ages_w(self):
        return self.__dates_ages_w

    def set_dates_ages_w(self):
        '''
        Creates all dates and ages from y to the largest w, expectedly the mortality table's w.
        '''
        # careful when counting years because of the actuarial ages
        max_w = [t[1].w for t in self.multi_table.unidecrement_tables.items()]
        max_w = max(max_w)
        dates_ages_w = [(age.Age(date1=self.date_of_valuation,
                                 date2=self.date_of_valuation).date_inc_years(j).date2.year, self.x + j)
                        for j in range(-self.past_time_service_years, max_w - self.x + 1)]
        self.__dates_ages_w = dates_ages_w

    @property
    def profile(self):
        print({'DoB': self.date_of_birth, 'DoE': self.date_of_entry, 'DoV': self.date_of_valuation,
               'Age@Entry': round(self.y_, 5), 'AAge@1Valuation': self.y,
               'Age@Valuation': round(self.age_date_of_valuation.age_f()[3], 5), 'AAge@Valuation': self.x,
               'AAge@TermCost': self.age_of_term_cost, 'waiting': self.waiting,
               'AAge@1Payment': self.age_first_payment,
               'Past Time Service': self.past_time_service_years,
               'Future Time Service': self.future_time_service_years,
               'Total Time Service': self.total_time_service_years})

    def prob_survival(self, x1, x2):
        '''
        We compute the probability of survival from today (x) until age x, used to project liabilities,
        considering that the decrement occurred, that is, considering that (x) will enter the state
        defined by the decrement.
        :param x1: initial age
        :param x2: final age
        :return: The probability of survival considering all the decrements
        '''
        if x2 <= x2: return 1
        if x2 < self.age_of_term_cost:
            tpx_T = self.multi_table.net_table.tpx(x1, t=x2 - x1, method='udd')
        else:
            bool_decrement = bool(self.decrement)
            tpx_T = self.multi_table.net_table.tpx(x1, t=self.age_of_term_cost - x1 - bool_decrement,
                                                   method='udd') * \
                    self.multi_table.unidecrement_tables['mortality'].tpx(self.age_of_term_cost,
                                                                          t=x2 - self.age_of_term_cost, method='udd')
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

    def pvftc_proj(self, x, px):
        '''
        Computes the Present Value of a Future Term Cost, that will allow us to use for all amortization schemes
        :param x: the age for life x. We consider that x is alive and if the decrement happens, it will be moved to
        to the other state. Hence, if there is a waiting period between the decrement occurrence and the first payment
        x should already be placed in the state corresponding to the decrement.
        For instance, if the decrement is disability, immediately after the decrement, x is moved to the state of
        disable and do the waiting, if any, until the first payment.
        There are states where the decrement happens just due to survival up to that age, for instance, retirement.
        :param px: the age where we project
        :return: The Present Value of Future Benefits
        '''
        dif_ages = x - self.y
        pvftc = self.pvftc(x)
        p = self.prob_survival(x, px)

        d = {'entry_year': self.dates_ages_w[0][0], 'entry_age': self.y,
             'year': self.dates_ages_w[dif_ages][0], 'age': self.dates_ages_w[dif_ages][1],
             'year_p': self.dates_ages_w[dif_ages][0], 'age_p': self.dates_ages_w[dif_ages][1],
             'age_of_term_cost': self.age_of_term_cost, 'age_first_payment': self.age_first_payment,
             'past_time_service_years': self.past_time_service_years + x - self.x,
             'futute_time_service_years': self.future_time_service_years - (x - self.x),
             'pvftc': pvftc, 'prob_surv_px': p, 'pvftc_p': pvftc * p}
        return d

    def sum_pvftc_proj(self, x, px, age_of_term_cost_init, age_of_term_cost_final, waiting=0):
        lst_tc_pj = []
        ages_term_costs = list(range(age_of_term_cost_init, age_of_term_cost_final + 1))
        for atc in ages_term_costs:
            self.age_of_term_cost = atc
            self.set_waiting_period(w=waiting)
            lst_tc_pj.append(self.pvftc_proj(x, px))
        return lst_tc_pj
