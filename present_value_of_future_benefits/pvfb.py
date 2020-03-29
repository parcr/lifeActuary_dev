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
        self.multi_table = None
        self.decrement = None
        self.i = i / 100,
        self.age_first_instalment = None
        self.age_last_instalment = None
        self.age_first_payment = None

        self.age_date_of_entry_ = age.Age(date1=date_of_birth, date2=date_of_entry)
        self.age_date_of_valuation_ = age.Age(date1=self.date_of_birth, date2=self.date_of_valuation)
