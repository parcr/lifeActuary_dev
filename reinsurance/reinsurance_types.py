'''
Quota-share
'''


class QuotaShare:
    def __init__(self, cedant_share, total_capacity, capital_at_risk):
        self.cedant_share = cedant_share
        self.total_capacity = total_capacity
        self.capital_at_risk = capital_at_risk

        self.reinsurer_share
        self.cedant_capacity
        self.reinsurer_capacity

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.cedant_share}, {self.total_capacity}, {self.capital_at_risk})"

    @property
    def cedant_share(self):
        return self.__cedant_share

    @cedant_share.setter
    def cedant_share(self, sc):
        if sc < 0:
            self.__cedant_share = 0
        if sc > 1:
            self.__cedant_share = 1
        self.__cedant_share = sc


    @property
    def total_capacity(self):
        return self.__total_capacity

    @total_capacity.setter
    def total_capacity(self, tc):
        if tc < 0:
            self.__total_capacity = 0
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
    def reinsurer_share(self):
        return 1 - self.cedant_share

    @property
    def cedant_capacity(self):
        return self.total_capacity*(1 - self.cedant_share)

    @property
    def reinsurer_capacity(self):
        return self.total_capacity - self.cedant_capacity

    def cedant_claim(self, claim):
        if claim < 0:
            return 0
        return min(claim, self.capital_at_risk) * self.__cedant_share

    def reinsurer_claim(self, claim):
        return claim - self.cedant_claim(claim)


class Surplus:
    def __init__(self, cedant_line, total_capacity, capital_at_risk):
        self.cedant_line = cedant_line
        self.total_capacity = total_capacity
        self.capital_at_risk = capital_at_risk

        self.reinsurer_capacity
        self.cedant_share

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.cedant_line}, {self.total_capacity}, {self.capital_at_risk})"

    @property
    def cedant_line(self):
        return self.__cedant_line

    @cedant_line.setter
    def cedant_line(self, lc):
        if lc < 0:
            self.__cedant_line = 0
        self.__cedant_line = lc
        try:
            self.total_capacity = self.__total_capacity
        except:
            pass

    @property
    def total_capacity(self):
        return self.__total_capacity

    @total_capacity.setter
    def total_capacity(self, tc):
        if tc < self.cedant_line:
            self.__total_capacity = self.cedant_line
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
        return self.total_capacity - self.cedant_line

    @property
    def reinsurer_lines(self):
        return self.reinsurer_capacity / self.cedant_line

    @property
    def cedant_share(self):
        if self.capital_at_risk>self.cedant_line:
            return self.cedant_line/self.capital_at_risk
        return 1

    @property
    def reinsurer_share(self):
        return 1-self.cedant_share

    def cedant_claim(self, claim):
        if claim < 0:
            return 0
        if claim <= self.cedant_line:
            return claim
        return 0

    def reinsurer_claim(self, claim):
        return claim - self.cedant_claim(claim)
