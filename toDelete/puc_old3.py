__author__ = "PedroCR"


class PUC:
    def __init__(self, x, age_first_instalment, age_last_instalment):
        self.x = x
        self.age_first_instalment = age_first_instalment
        self.age_last_instalment = age_last_instalment
        self.set_total_time_service_nc()

    @property
    def age_first_instalment(self):
        return self.__age_first_instalment

    @age_first_instalment.setter
    def age_first_instalment(self, afi):
        self.__age_first_instalment = afi
        self.set_total_time_service_nc()

    @property
    def age_last_instalment(self):
        return self.__age_of_last_instalment

    @age_last_instalment.setter
    def age_last_instalment(self, ali):
        self.__age_of_last_instalment = ali
        self.set_total_time_service_nc()

    def past_time_service_nc(self):
        '''
        computes past time service at age x for the normal contributions, that is the instalments
        '''
        if self.age_first_instalment < self.x <= self.age_last_instalment:
            return self.x - self.age_first_instalment
        if self.x > self.age_last_instalment:
            return self.age_last_instalment + 1 - self.age_first_instalment
        return 0

    def future_time_service_nc(self):
        '''
        computes future time service at age x for the normal contributions, that is the instalments
        '''
        return (self.age_last_instalment + 1 - self.age_first_instalment) - self.past_time_service_nc()

    @property
    def total_time_service_nc(self):
        return self.__total_time_service_nc

    def set_total_time_service_nc(self):
        if self.age_first_instalment is not None and self.age_last_instalment is not None:
            self.__total_time_service_nc = self.age_last_instalment + 1 - self.age_first_instalment
        else:
            self.__total_time_service_nc = None

    def future_nc(self):
        return self.age_last_instalment - self.x
