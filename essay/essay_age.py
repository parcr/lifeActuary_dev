__author__ = "PedroCR"

import age
import numpy as np
import datetime
import calendar
from dateutil.relativedelta import relativedelta

sd = '1956-12-24'
sd2 = '1841-03-02'
sd3 = '2000/04-23'

d1 = datetime.date(2000, 4, 23)
d2 = datetime.date(2002, 7, 18)
a = age.Age(d1, d2)
print(f"Age for {a} is {a.age_f()[0]} years, {a.age_f()[1]} months and {a.age_f()[2]} days,"
      f" that is, {a.age_f()[3]} years")

d1 = datetime.date(1968, 2, 14)
d2 = datetime.date.today()
a = age.Age(d1, d2)
print(f"Age for {a} is {a.age_f()[0]} years, {a.age_f()[1]} months and {a.age_f()[2]} days,"
      f" that is, {a.age_f()[3]} years")
