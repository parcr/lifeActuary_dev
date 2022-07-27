import numpy as np
import sympy as sym
import IPython.display as disp
from scipy.stats import expon

sym.init_session(quiet=True)
sym.init_printing(use_latex='mathjax')

print('derivative test')
rv = expon(0, 1)
mean, var, skew, kurt = rv.stats(moments='mvsk')

print(f"For sub-portfolio A, we've mean={mean}, variance={var}, skewness={skew} and kurtosis={kurt}")
print('min value is:', rv.ppf(0))

lmbda, x = sym.symbols("lmbda, x", real=True)
dlta = sym.symbols('dlta', real=True, positive=True)


def rv_sym(lmbda, dlta, x):
    return sym.exp(-(x-lmbda)/dlta)/dlta


disp.display(rv_sym(2, 1, x))
a=sym.integrate(rv_sym(2, 1, x)*x, (x,2,np.infty))
