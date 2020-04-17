__author__ = "PedroCR"

from essential_life import age
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

sd = '1956-12-24'
sd2 = '1841-03-02'
sd3 = '2000/04-23'

d1 = datetime.date(2000, 4, 23)
d2 = datetime.date(2002, 7, 18)
a = age.Age(d1, d2)
print(f"Age for {a} is {a.age_f()[0]} years, {a.age_f()[1]} months and {a.age_f()[2]} days,"
      f" that is, {a.age_f()[3]} years")


d1 = datetime.date(1968, 2, 14)
d2 = datetime.datetime.now()
print(relativedelta(d2, d1))
a = age.Age(d1, d2)
print(f"Age for {a} is {a.age_f()[0]} years, {a.age_f()[1]} months and {a.age_f()[2]} days,"
      f" that is, {a.age_f()[3]} years")

d1 = "1968-02-14"
d2 = datetime.date.today()
print(a.age_f())
print((pd.to_datetime(d2) - pd.to_datetime(d1)))

# test error
sd4 = "1950-03-230"
sd5 = "1950-03/23"
a.date1 = sd4
a.date2 = sd5
