# author: PedroCR #
import numpy as np
import datetime
import calendar
from dateutil.relativedelta import relativedelta


class Age(object):
    """ class to instantiate forms of computing the time difference, based on  2 dates"""

    def __new__(cls, date1, date2):
        """
        :param date1: First date to compute the difference, the minuend
        :param date2: Second date to compute the difference, the subtrahend
        """
        is_date1 = False
        is_date2 = False
        if isinstance(cls.create_date(date1), datetime.date):
            is_date1 = True
        if isinstance(cls.create_date(date2), datetime.date):
            is_date2 = True

        if is_date1 and is_date2:
            # print('ok to instantiate')
            return object.__new__(cls)
        elif not is_date1 and is_date2:
            print(f"We could't parse {date1} to date")
            return None
        elif is_date1 and not is_date2:
            print(f"We could't parse {date2} to date")
            return None
        else:
            print(f"We could't parse neither {date1} and {date2} to date")
            return None

    def __init__(self, date1, date2):
        """
        :param date1: First date to compute the difference, the minuend
        :param date2: Second date to compute the difference, the subtrahend
        """
        if isinstance(self.create_date(date1), datetime.date) and isinstance(self.create_date(date2), datetime.date):
            self.__date1 = self.create_date(date1)
            self.__date2 = self.create_date(date2)
        else:
            print('Construction failed @ __init__!')

    def __del__(self):
        print('Object killed')

    def __repr__(self) -> str:
        return f"Age('{self.__date1}', '{self.__date2}')"

    # def __str__(self):
    #     return '{0}({1})'.format(self.__class__.__name__, self.__dict__)

    @staticmethod
    def create_date(s):
        """
        :param s: receives a string
        :return: an instance of datetime as date created from :param s
        """
        if isinstance(s, datetime.date):
            return s
        else:  # try to create a date from a string
            forms = ['%Y-%m-%d', '%Y/%m/%d']
            err_str = str(s) + ' as a Date is not in any of the formats:'
            tries = []

            for f in forms:
                try:
                    d = datetime.datetime.strptime(str(s), f)
                except ValueError as excep:
                    tries.append(f)
                else:
                    return datetime.date(d.year, d.month, d.day)
        if tries:
            print(err_str, tries)

    @property
    def date1(self):
        return self.__date1

    @date1.setter
    def date1(self, d):
        if isinstance(d, datetime.date):
            self.__date1 = d
        elif isinstance(d, str) and isinstance(self.create_date(d), datetime.date):
            self.__date1 = self.create_date(d)
        else:
            raise TypeError('We need an instance of datetime.')

    @date1.deleter
    def date1(self):
        del self.__date1

    @property
    def date2(self):
        return self.__date1

    @date2.setter
    def date2(self, d):
        if isinstance(d, datetime.date):
            self.__date2 = d
        elif isinstance(d, str) and isinstance(self.create_date(d), datetime.date):
            self.__date2 = self.create_date(d)
        else:
            raise TypeError('We need an instance of datetime.')

    @date2.deleter
    def date2(self):
        del self.__date2

    def age_f(self):
        """
        :return: dif_years as int, dif_months as int, dif_days as int & the age in years as float
        """
        dif_years = relativedelta(self.__date2, self.__date1).years
        dif_months = relativedelta(self.__date2, self.__date1).months
        dif_days = relativedelta(self.__date2, self.__date1).days
        if calendar.isleap(self.__date2.year):
            return dif_years, dif_months, dif_days, dif_years + dif_months / 12 + dif_days / 366
        else:
            return dif_years, dif_months, dif_days, (dif_years + dif_months / 12 + dif_days / 365)

    def age_act(self):
        """
        :return: The actuarial age, that is the closest integer age, obtained by rounding self.age_f()
        """
        return np.int(np.floor(self.age_f()[-1] + .5))

    def date_inc_years(self, years):
        """
        Increments years to date2 so that the actuarial age is increased by years
        :param years: years to increase to the age of the object
        :return: a new instance of Age with date2 equal to years in date2+years
        """
        if isinstance(years, int):
            return Age(self.__date1, self.__date2 + relativedelta(years=years))


# Examples
sd = '1956-12-24'
sd2 = '1841-03-02'
sd3 = '2000/04-23'

d1 = datetime.date(2000, 4, 23)
d2 = datetime.date(2002, 7, 18)
a = Age(d1, d2)
