'''
Quota-share
'''


class QuotaShare:
    def __init__(self, share_cedant, cedant_capacity, total_capacity, capital_at_risk):
        self.share_cedant = share_cedant
        self.cedant_capacity = cedant_capacity
        self.total_capacity = total_capacity
        self.capital_at_risk = capital_at_risk

        self.reinsurer_capacity

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.share_cedant}, {self.cedant_capacity}, {self.total_capacity}," \
               f"{self.capital_at_risk})"

    @property
    def share_cedant(self):
        return self.__share_cedant

    @share_cedant.setter
    def share_cedant(self, sc):
        if sc < 0:
            self.__share_cedant = 0
        if sc > 1:
            self.__share_cedant = 1
        self.__share_cedant = sc

    @property
    def cedant_capacity(self):
        return self.__cedant_capacity

    @cedant_capacity.setter
    def cedant_capacity(self, cc):
        if cc < 0:
            self.__cedant_capacity = 0
        self.__cedant_capacity = cc
        try:
            self.total_capacity = self.__total_capacity
        except:
            pass

    @property
    def total_capacity(self):
        return self.__total_capacity

    @total_capacity.setter
    def total_capacity(self, tc):
        if tc < self.cedant_capacity:
            self.__total_capacity = self.cedant_capacity
        else:
            self.__total_capacity = tc

    @property
    def capital_at_risk(self):
        return self.__capital_at_risk

    @capital_at_risk.setter
    def capital_at_risk(self, cr):
        if cr < 0:
            self.__capital_at_risk = 0
        self.__capital_at_risk = min(cr, self.__total_capacity)

    @property
    def reinsurer_capacity(self):
        return self.total_capacity - self.cedant_capacity

    def cedant_claim(self, claim):
        if claim < 0:
            return 0
        return min(claim, self.capital_at_risk) * self.__share_cedant

    def reinsurer_claim(self, claim):
        return claim - self.cedant_claim(claim)


qs = QuotaShare(.2, 1000, 10000, 2000)
