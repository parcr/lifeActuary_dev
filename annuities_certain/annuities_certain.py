import numpy as np


class Annuities_Certain:
    '''

    '''
    def __init__(self, interest_rate, m=1):
        '''

        :param interest_rate:
        :param m:
        '''
        self.interest_rate = interest_rate / 100.
        self.frequency = m

        self.v = 1 / (1 + self.interest_rate)
        self.im = self.frequency * (np.power(1 + self.interest_rate, 1 / self.frequency) - 1)
        self.vm = np.power((1 + self.im / self.frequency), -1)
        self.dm = self.im * self.vm

    def aan(self, terms):
        '''

        :param terms:
        :return:
        '''
        if not terms:
            return 1 / self.dm
        return (1 - np.power(self.vm, terms * self.frequency)) / self.dm

    def an(self, terms):
        '''

        :param terms:
        :return:
        '''
        if not terms:
            return 1 / self.im
        return (1 - np.power(self.vm, terms * self.frequency)) / self.im

    # todo: Rita
    def Iaan(self, terms, payment=1, increase=1):
        '''

        :param terms:
        :param payment:
        :param increase:
        :return:
        '''
        self.Iman(terms, payment, increase) / self.vm

    # todo: Rita
    def Iman(self, terms, payment=1, increase=1):
        '''

        :param terms:
        :param payment:
        :param increase:
        :return:
        '''
        if payment + increase * terms < 0:
            return np.nan

        return (payment - increase) * self.an(terms) \
               + increase * self.v \
               * (self.v ** terms * ((terms * self.frequency) * (self.vm - 1) - 1) + 1) \
               / (self.frequency * self.v ** ((self.frequency - 1) / self.frequency) * (self.vm - 1) ** 2)

    # todo: Rita & Pedro
    def Ian(self, terms, payment=1, increase=1):
        '''

        :param terms:
        :param payment:
        :param increase:
        :return:
        '''
        if payment + increase * terms < 0:
            return np.nan
        # (payment - increase) * self.an(terms) + increase * (self.aan(terms) - terms * self.v ** terms) / self.im
        return payment*self.an(terms)+increase/self.im*((1-self.v**terms)/self.interest_rate-terms*self.v**terms)

    # todo: Rita
    def Gaan(self, terms, payment=1, grow=0):
        '''

        :param terms:
        :param payment:
        :param grow:
        :return:
        '''
        v = (1 + grow / 100) * self.v
        return self.Gan(terms, payment, grow) / v ** (1 / self.frequency)

    # todo: Rita
    def Gan(self, terms, payment=1, grow=0):
        '''

        :param terms:
        :param payment:
        :param grow:
        :return:
        '''
        v = (1 + grow / 100) * self.v
        return payment / (1 + grow / 100) ** (1 / self.frequency) * (1 - v ** terms) / (
                1 - v ** (1 / self.frequency)) * v ** (1 / self.frequency)
