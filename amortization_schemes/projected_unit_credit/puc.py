__author__ = "PedroCR"

from essential_life.time_services import TimeServices


class PUC:
    def __init__(self, age, age_first_instalment, age_last_instalment):
        self.age = age
        self.age_first_instalment = age_first_instalment
        self.age_last_instalment = age_last_instalment
        self.__set_ts()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.age}, {self.age_first_instalment}, {self.age_last_instalment})"

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, x):
        self.__age = x
        try:
            self.__ts = TimeServices(age=self.age, first_age=self.age_first_instalment,
                                     last_age=self.age_last_instalment)
        except AttributeError as ae:
            pass

    @property
    def age_first_instalment(self):
        return self.__age_first_instalment

    @age_first_instalment.setter
    def age_first_instalment(self, x):
        self.__age_first_instalment = x
        try:
            self.__ts = TimeServices(age=self.age, first_age=self.age_first_instalment,
                                     last_age=self.age_last_instalment)
        except AttributeError as ae:
            pass

    @property
    def age_last_instalment(self):
        return self.__age_last_instalment

    @age_last_instalment.setter
    def age_last_instalment(self, x):
        self.__age_last_instalment = x
        try:
            self.__ts = TimeServices(age=self.age, first_age=self.age_first_instalment,
                                     last_age=self.age_last_instalment)
        except AttributeError as ae:
            pass

    @property
    def ts(self):
        return self.__ts

    def __set_ts(self):
        self.__ts = TimeServices(age=self.age, first_age=self.age_first_instalment,
                                 last_age=self.age_last_instalment)

    def al(self):
        if self.age <= self.age_first_instalment:
            return 0
        return (self.ts.past_time_service + 1) / self.ts.total_periods

    def nc(self):
        if self.age_first_instalment <= self.age <= self.age_last_instalment:
            return 1 / self.ts.total_periods
        return 0
