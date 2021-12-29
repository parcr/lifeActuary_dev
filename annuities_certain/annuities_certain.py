import numpy as np


class Annuities_Certain:
    def __init__(self, interest_rate, frequency=1):
        self.interest_rate = interest_rate / 100.
        self.frequency = frequency

        self.i_m = self.frequency * (np.power(1 + self.interest_rate, 1 / self.frequency) - 1)
        self.v_m = np.power((1 + self.i_m / self.frequency), -1)
        self.d_m = self.i_m * self.v_m

    def annuity_due(self, terms):
        if not terms:
            return 1 / self.d_m
        return (1 - np.power(self.v_m, terms * self.frequency)) / self.d_m

    def annuity_immediate(self, terms):
        if not terms:
            return 1 / self.i_m
        return (1 - np.power(self.v_m, terms * self.frequency)) / self.i_m
