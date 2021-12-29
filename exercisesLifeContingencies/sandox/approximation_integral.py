import scipy.integrate
import scipy.special as sc
import numpy as np


def f(x):
    return np.exp(-x) / x


# call quad to integrate f from -2 to 2
res, err = scipy.integrate.quad(f, 0, np.inf)

print("The numerical result is {:f} (+-{:g})".format(res, err))

res = sc.gammaincc(0.5, 1)
res_2 = sc.expi(.5)
print(f"The numerical result is {res}")
print(f"The numerical result is {res_2}")

'''
Gompertz Law
'''
# https://www.integral-calculator.com/#expr=exp%28-b%2Fln%28c%29c%5Ex%28c%5Et-1%29%29&intvar=t
b = 0.0003
c = 1.07


def moments_Tx(b, c, x=0, k=1):
    if x < 0:
        return np.nan
    if k == 0:
        return 1
    elif k == 1:
        u = b * np.power(c, x) / np.log(c)
        e1 = sc.expi(u)
        return -np.exp(u) / np.log(c) * e1


x = 0


def expected_value_Tx(b, c, x=0):
    return moments_Tx(b, c, x, k=1)


a = expected_value_Tx(b=b, c=c, x=x)
print('Expected value:', a)


def f(x):
    return np.exp(-x) / x * np.exp(u) / np.log(c)


u = b * np.power(c, x) / np.log(c)
ev = scipy.integrate.quad(f, u, np.inf)


def t_pxt(t):
    return t*np.exp(-b / np.log(c) * np.power(c, x) * (np.power(c, t) - 1))


ev2 = scipy.integrate.quad(t_pxt, 0, np.inf)
