__author__ = "PedroCR"

from present_value_future_term_cost.pvftc import PVTermCost


class PUC(PVTermCost):
    def __init__(self, date_of_valuation, date_of_birth, date_of_entry,
                 age_of_term_cost, waiting=0,
                 multi_table=None, decrement=None,
                 i=None,
                 age_first_instalment=None, age_last_instalment=None):
        PVTermCost.__init__(self, date_of_valuation, date_of_birth, date_of_entry,
                            age_of_term_cost, waiting,
                            multi_table, decrement,
                            i)
        self.age_first_instalment = age_first_instalment
        self.age_last_instalment = age_last_instalment
        self.total_time_service_nc = -1

    @property
    def age_first_instalment(self):
        return self.__age_first_instalment

    @age_first_instalment.setter
    def age_first_instalment(self, afi):
        if afi is None:
            self.__age_first_instalment = self.y
        else:
            self.__age_first_instalment = afi

    @property
    def age_last_instalment(self):
        return self.__age_of_last_instalment

    @age_last_instalment.setter
    def age_last_instalment(self, ali):
        if ali is None:
            self.__age_of_last_instalment = self.age_of_term_cost - 1
        else:
            self.__age_first_instalment = ali

    @property
    def past_time_service_nc(self, x=None):
        '''
        computes past time service at age x for the normal contributions, that is the instalments
        '''
        if x is None: x = self.x
        if self.age_first_instalment < x <= self.age_last_instalment:
            return x - self.age_first_instalment
        if x > self.age_last_instalment:
            return self.age_last_instalment + 1 - self.age_first_instalment
        return 0

    def future_time_service_nc(self, x=None):
        '''
        computes future time service at age x for the normal contributions, that is the instalments
        '''
        return (self.age_last_instalment + 1 - self.age_first_instalment) - self.past_time_service_nc(x)

    @property
    def total_time_service_nc(self):
        return self.__total_time_service_nc

    @total_time_service_nc.setter # todo: Estou aqui
    def total_time_service_nc(self):
        self.age_last_instalment + 1 - self.age_first_instalment

    def future_nc(self, x=None):
        return self.age_last_instalment - x

    def al(self, x):
        if x > self.age_first_instalment:
            return self.pvftc(x=x) * self.past_time_service_nc() / \
                   (self.past_time_service_nc() + self.future_time_service_nc())
        return 0

    def nc(self, x):
        if x >= self.age_first_instalment:
            return self.pvftc(x=x) / \
                   (self.past_time_service_nc() + self.future_time_service_nc())
        return 0

    '''
    Testing if the method allows for a correct and full amortization
    '''

    '''
    Projections
    '''
