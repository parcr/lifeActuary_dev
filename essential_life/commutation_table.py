__author__ = "PedroCR"

import numpy as np
import pandas as pd
from essential_life.mortality_table import MortalityTable


# todo: confirm all the messages
class CommutationFunctions(MortalityTable):
    '''
    Instantiates a for a specific mortality table and interest rate, all the usual commutation functions.
    '''

    def __init__(self, i=None, g=0, data_type='q', mt=None, perc=100, app_cont=False):
        MortalityTable.__init__(self, data_type, mt, perc)
        if i is None:
            return
        self.__i = i / 100.
        self.__g = g / 100.
        self.__v = 1 / (1 + self.__i)
        self.__d = (1 + self.__g) / (1 + self.__i)
        self.__app_cont = app_cont
        self.__cont = np.sqrt(1 + self.__i)

        # self.__Dx = np.array([self.lx[x] * np.power(self__d, x) for x in range(len(self.lx))])
        self.__Dx = self.lx[:-1] * np.power(self.__d, range(len(self.lx[:-1])))
        self.__Nx = np.array([np.sum(self.__Dx[x:]) for x in range(len(self.lx[:-1]))])
        self.__Sx = np.array([np.sum(self.__Nx[x:]) for x in range(len(self.__Nx))])
        self.__Cx = self.dx * np.power(self.__d, range(1, len(self.dx) + 1))
        self.__Mx = np.array([np.sum(self.__Cx[x:]) for x in range(len(self.__Cx))])
        self.__Rx = np.array([np.sum(self.__Mx[x:]) for x in range(len(self.__Mx))])
        if self.__app_cont:
            self.__Mx = self.__Mx * self.__cont
            self.__Rx = self.__Rx * self.__cont

    def __repr__(self):
        return f"{self.__class__.__name__}{self.i, self.g, self.data_type, self.mt, self.perc, self.app_cont}"

    # getters and setters
    @property
    def i(self):
        return self.__i * 100

    @property
    def g(self):
        return self.__g * 100

    @property
    def v(self):
        return self.__v

    @property
    def d(self):
        return self.__d

    @property
    def app_cont(self):
        return self.__app_cont

    @property
    def cont(self):
        return self.__cont

    @property
    def Dx(self):
        return self.__Dx

    @property
    def Nx(self):
        return self.__Nx

    @property
    def Sx(self):
        return self.__Sx

    @property
    def Cx(self):
        return self.__Cx

    @property
    def Mx(self):
        return self.__Mx

    @property
    def Rx(self):
        return self.__Rx

    def df_commutation_table(self):
        data = {'Dx': self.__Dx, 'Nx': self.__Nx, 'Sx': self.__Sx, 'Cx': self.__Cx, 'Mx': self.__Mx, 'Rx': self.__Rx}
        df = pd.DataFrame(data)
        data_lf = self.df_life_table()
        df = pd.concat([data_lf, df], axis=1, sort=False)
        return df

    # life insurances
    def nEx(self, x, n):
        """
        Pure endowment or Deferred capital
        :param x: age at the beginning of the contract
        :param n: years until payment, if x is alive
        :return: the present value of a pure endowment of 1 at age x+n
        """
        if x < 0:
            return np.nan
        if n <= 0:
            return 1
        if x + n > self.w:
            return 0.
        D_x = self.__Dx[x]
        D_x_n = self.__Dx[x + n]
        self.msn.append(f"{n}_E_{x}={D_x_n} / {D_x}")
        # note: nEx discounts the growth rate np.power(1 + self.__g, defer + 1) so only survival is considered
        return D_x_n / D_x / np.power(1 + self.__g, n)

    def Ax(self, x):
        """
        Whole life insurance
        :param x: age at the beginning of the contract
        :return: Expected Present Value (EPV) of a whole life insurance (i.e. net single premium), that pays 1, at the
        end of the year of death. It is also commonly referred to as the Actuarial Value or Actuarial Present Value.
        """
        if x < 0:
            return np.nan
        if x > self.w:
            return self.__v  # it will die before year's end, because already attained age>w
        D_x = self.__Dx[x]
        if self.__app_cont:
            M_x = self.__Mx[x] / self.__cont
        else:
            M_x = self.__Mx[x]
        self.msn.append(f"A_{x}={M_x} / {D_x}")
        return M_x / D_x / (1 + self.__g)

    def IAx(self, x):
        """
        Whole life insurance
        :param x: age at the beginning of the contract
        :return: Expected Present Value (EPV) of a whole life insurance (i.e. net single premium), that pays 1+m, at the
        end of the year of death, if death happens between age x+m and x+m+1.
        It is also commonly referred to as the Actuarial Value or Actuarial Present Value.
        """
        if x < 0:
            return np.nan
        if x > self.w:
            return self.__v  # it will die before year's end, because already attained age>w
        D_x = self.__Dx[x]
        if self.__app_cont:
            R_x = self.__Rx[x] / self.__cont
        else:
            R_x = self.__Rx[x]
        self.msn.append(f"A_{x}={R_x} / {D_x}")
        return R_x / D_x

    def Ax_(self, x):
        """
        Whole life insurance
        :param x: age at the beginning of the contract
        :return: Expected Present Value (EPV) of a whole life insurance (i.e. net single premium), that pays 1, at the
        moment of death. It is also commonly referred to as the Actuarial Value or Actuarial Present Value.
        """
        if x < 0:
            return np.nan
        if x > self.w:  # it will die before year's end, because already attained age>w
            return self.__v ** .5
        D_x = self.__Dx[x]
        if self.__app_cont:
            M_x = self.__Mx[x]
        else:
            M_x = self.__Mx[x] * self.__cont
        self.msn.append(f"A_{x}_={M_x} / {D_x}")
        return M_x / D_x / (1 + self.__g)

    def nAx(self, x, n):
        """
        Term life insurance
        :param x: age at the beginning of the contract
        :param n: period of the contract
        :return: Expected Present Value (EPV) of a term (temporary) life insurance (i.e. net single premium), that
        pays 1, at the end of the year of death. It is also commonly referred to as the Actuarial Value or
        Actuarial Present Value.
        """
        if x < 0:
            return np.nan
        if n < 0:
            return np.nan
        if x + n > self.w:
            return self.Ax(x)
        D_x = self.__Dx[x]
        if self.__app_cont:
            M_x = self.__Mx[x] / self.__cont
            M_x_n = self.__Mx[x + n] / self.__cont
        else:
            M_x = self.__Mx[x]
            M_x_n = self.__Mx[x + n]
        self.msn.append(f"{n}_A_{x}=({M_x}-{M_x_n}) / {D_x}")
        return (M_x - M_x_n) / D_x / (1 + self.__g)

    def nIAx(self, x, n):
        """
        Whole life insurance
        :param x: age at the beginning of the contract
        :param n: period of the contract
        :return: Expected Present Value (EPV) of a whole life insurance (i.e. net single premium), that pays 1+m, at the
        end of the year of death, if death happens between age x+m and x+m+1.
        It is also commonly referred to as the Actuarial Value or Actuarial Present Value.
        """
        if x < 0:
            return np.nan
        if n < 0:
            return np.nan
        if x > self.w:
            return self.__v  # it will die before year's end, because already attained age>w
        D_x = self.__Dx[x]
        if self.__app_cont:
            M_x_n = self.__Mx[x + n] / self.__cont
            R_x = self.__Rx[x] / self.__cont
            R_x_n = self.__Rx[x + n] / self.__cont
        else:
            M_x_n = self.__Mx[x + n]
            R_x = self.__Rx[x]
            R_x_n = self.__Rx[x + n]
        self.msn.append(f"A_{x}=({R_x}-{R_x_n}-{n}x{M_x_n} / {D_x}")
        return (R_x - R_x_n - n * M_x_n) / D_x

    def nAx_(self, x, n):
        """
        Term life insurance
        :param x: age at the beginning of the contract
        :param n: period of the contract
        :return: Expected Present Value (EPV) of a term (temporary) life insurance (i.e. net single premium), that
        pays 1, at the moment of death. It is also commonly referred to as the Actuarial Value or
        Actuarial Present Value.
        """
        if x < 0:
            return np.nan
        if n < 0:
            return np.nan
        if x + n > self.w:
            return self.Ax(x) * self.__cont
        D_x = self.__Dx[x]
        if self.__app_cont:
            M_x = self.__Mx[x]
            M_x_n = self.__Mx[x + n]
        else:
            M_x = self.__Mx[x] * self.__cont
            M_x_n = self.__Mx[x + n] * self.__cont
        self.msn.append(f"{n}_A_{x}_=({M_x}-{M_x_n}) / {D_x}")
        return (M_x - M_x_n) / D_x / (1 + self.__g)

    def nAEx(self, x, n):
        """
        Endowment insurance
        :param x: age at the beginning of the contract
        :param n: period of the contract
        :return: Expected Present Value (EPV) of an Endowment life insurance (i.e. net single premium), that
        pays 1, at the end of year of death or 1 if x survives to age x+n. It is also commonly referred to as the
        Actuarial Value or Actuarial Present Value.
        """
        self.msn.append(f"{n}_AE_{x}={n}_A_{x}+{n}_E_{x}")
        return self.nAx(x, n) + self.nEx(x, n)

    def nAEx_(self, x, n):
        """
        Endowment insurance
        :param x: age at the beginning of the contract
        :param n: period of the contract
        :return: Expected Present Value (EPV) of an Endowment life insurance (i.e. net single premium), that
        pays 1, at the moment of death or 1 if x survives to age x+n. It is also commonly referred to as the
        Actuarial Value or Actuarial Present Value.
        """
        aux = self.nAx_(x, n) + self.nEx(x, n)
        self.msn.append(f"{n}_AE_{x}_={n}_A_{x}_+{n}_E_{x}")
        return aux

    # deferred life insurances
    def t_Ax(self, x, defer=0):
        """
        Deferred Whole life insurance
        :param x: age at the beginning of the contract
        :param defer: deferment period
        :return: Expected Present Value (EPV) of a whole life insurance (i.e. net single premium), that pays 1,at the
        end of the year of death. It is also commonly referred to as the Actuarial Value or Actuarial Present Value.
        """
        aux = self.nEx(x, defer) * self.Ax(x + defer)
        self.msn.append(f"{defer}|_A_{x}={defer}_E_{x}*A_{x + defer}")
        return aux

    def t_Ax_(self, x, defer=0):
        """
        Deferred Whole life insurance
        :param x: age at the beginning of the contract
        :param defer: deferment period
        :return: Expected Present Value (EPV) of a whole life insurance (i.e. net single premium), that pays 1, at the
        moment of death. It is also commonly referred to as the Actuarial Value or Actuarial Present Value.
        """
        aux = self.nEx(x, defer) * self.Ax_(x + defer)
        self.msn.append(f"{defer}|_A_{x}_={defer}_E_{x}*A_{x + defer}_")
        return aux

    def t_nAx(self, x, n, defer=0):
        """
        Deferred Term life insurance
        :param x: age at the beginning of the contract
        :param n: period of the contract
        :param defer: deferment period
        :return: Expected Present Value (EPV) of a term (temporary) life insurance (i.e. net single premium), that
        pays 1, at the end of the year of death. It is also commonly referred to as the Actuarial Value or
        Actuarial Present Value.
        """
        aux = self.nEx(x, defer) * self.nAx(x + defer, n)
        self.msn.append(f"{defer}|{n}_A_{x}={defer}_E_{x}*{n}_A_{x + defer}")
        return aux

    def t_nAx_(self, x, n, defer=0):
        """
        Deferred Term life insurance
        :param x: age at the beginning of the contract
        :param n: period of the contract
        :param defer: deferment period
        :return: Expected Present Value (EPV) of a term (temporary) life insurance (i.e. net single premium), that
        pays 1, at the moment of death. It is also commonly referred to as the Actuarial Value or
        Actuarial Present Value.
        """
        aux = self.nEx(x, defer) * self.nAx_(x + defer, n)
        self.msn.append(f"{defer}|{n}_A_{x}_={defer}_E_{x}*{n}_A_{x + defer}_")
        return aux

    def t_nAEx(self, x, n, defer=0):
        """
        Deferred Endowment insurance
        :param x: age at the beginning of the contract
        :param n: period of the contract
        :param defer: deferment period
        :return: Expected Present Value (EPV) of an Endowment life insurance (i.e. net single premium), that
        pays 1, at the end of year of death or 1 if x survives to age x+n. It is also commonly referred to as the
        Actuarial Value or Actuarial Present Value.
        """
        aux = self.nEx(x, defer) * self.nAEx(x + defer, n)
        self.msn.append(f"{defer}|{n}_AE_{x}={defer}_E_{x}*{n}_AE_{x + defer}")
        return aux

    def t_nAEx_(self, x, n, defer=0):
        """
        Deferred Endowment insurance
        :param x: age at the beginning of the contract
        :param n: period of the contract
        :param defer: deferment period
        :return: Expected Present Value (EPV) of an Endowment life insurance (i.e. net single premium), that
        pays 1, at the moment of death or 1 if x survives to age x+n. It is also commonly referred to as the
        Actuarial Value or Actuarial Present Value.
        """
        aux = self.nEx(x, defer) * self.nAEx_(x + defer, n)
        self.msn.append(f"{defer}|{n}_AE_{x}={defer}_E_{x}*{n}_AE_{x + defer}_")
        return aux

    # life annuities_1
    def ax(self, x, m=1):
        """
        axn : Returns the actuarial present value of an (immediate) annuity of 1 per time period
        (whole life annuity-late). Payable 'm' per year at the ends of the period Payable 'm' per year at the end of
        the period
        :param x: age at the beginning of the contract
        :param m: number of payments per period used to quote the interest rate
        :return:Expected Present Value (EPV) for payments of 1/m
        """
        if x < 0:
            return np.nan
        if m < 0:
            return np.nan
        if x >= self.w:
            return 0
        aux = self.__Nx[x + 1] / self.__Dx[x] / (1 + self.__g) + (m - 1) / (m * 2)
        self.msn.append(f"ax_{x}={self.__Nx[x + 1]}/{self.__Dx[x]}+({m}-1)/({m}*2)")
        return aux

    def aax(self, x, m=1):
        """
        äxn : Returns the actuarial present value of an (immediate) annuity of 1 per time period
        (whole life annuity-anticipatory). Payable 'm' per year at the beginning of the period
        :param x: age at the beginning of the contract
        :param m: number of payments per period used to quote the interest rate
        :return:Expected Present Value (EPV) for payments of 1/m
        """
        if x > self.w:
            return 1
        aux = self.__Nx[x] / self.__Dx[x] - (m - 1) / (m * 2)
        self.msn.append(f"aax_{x}={self.__Nx[x]}/{self.__Dx[x]}-({m}-1)/({m}*2)")
        return aux

    def nax(self, x, n, m=1):
        """
        axn : Return the actuarial present value of a (immediate) temporal (term certain) annuity: n-year temporary
        life annuity-late. Payable 'm' per year at the ends of the period
        :param x: age at the beginning of the contract
        :param n: number of total periods of the interest rate used
        :param m: number of payments per period used to quote the interest rate
        :return:Expected Present Value (EPV) for payments of 1/m
        """
        if x >= self.w:
            return 0
        if x < 0:
            return np.nan
        if m < 0:
            return np.nan
        if n < 0:
            return 0

        if x + 1 + n <= self.w:
            aux = (self.__Nx[x + 1] - self.__Nx[x + 1 + n]) / self.__Dx[x] / (1 + self.__g) + \
                  (m - 1) / (m * 2) * (1 - self.nEx(x, n))
            self.msn.append(f"{n}_ax_{x}={self.__Nx[x + 1] - self.__Nx[x + 1 + n]}/{self.__Dx[x]}+({m}-1)/({m}*2)*"
                            f"(1-{self.__Dx[x + n]}/{self.__Dx[x]})")
        else:
            return self.ax(x=x, m=m)

        return aux

    def naax(self, x, n, m=1):
        """
        näx : Return the actuarial present value of a (immediate) temporal (term certain) annuity: n-year temporary
        life annuity-anticipatory. Payable 'm' per year at the beginning of the period
        :param x: age at the beginning of the contract
        :param n: number of total periods of the interest rate used
        :param m: number of payments per period used to quote the interest rate
        :return:Expected Present Value (EPV) for payments of 1/m
        """
        if x >= self.w or n == 1:
            return 1
        if x < 0:
            return np.nan
        if m < 0:
            return np.nan
        if n < 0:
            return 0

        if x + 1 + n <= self.w + 1:  # todo we've here a problem, because of the fractional approximation
            aux = (self.__Nx[x] - self.__Nx[x + n]) / self.__Dx[x] - (m - 1) / (m * 2) * (1 - self.nEx(x, n))
            if x + 1 + n <= self.w:
                Nx2 = self.__Nx[x + 1 + n]
            else:
                Nx2 = 0
            self.msn.append(
                f"{n}_aax_{x}={self.__Nx[x + 1] - Nx2}/{self.__Dx[x]}*(1+{self.__g}) + ({m}+1)/({m}*2)*"
                f"(1-{self.__Dx[x + n]}/{self.__Dx[x]})")
        else:
            return self.aax(x=x, m=m)
        return aux

    # deferred annuities_1
    def t_ax(self, x, m=1, defer=0):
        """
        axn : Returns the actuarial present value of an (immediate) annuity of 1 per time period
        (whole life annuity-late), deferred t periods. Payable 'm' per year at the ends of the period Payable 'm'
        per year at the end of the period
        :param x: age at the beginning of the contract
        :param m: number of payments per period used to quote the interest rate
        :param defer: deferment period
        :return:Expected Present Value (EPV) for payments of 1/m
        """
        # note: nEx discounts the growth rate np.power(1 + self.__g, defer + 1)
        aux = self.ax(x + defer, m) * self.nEx(x, defer)
        if aux > 0:
            self.msn.append(f"{defer}_ax_{x}=[{self.__Nx[x + 1 + defer]}/{self.__Dx[x + defer]}+({m} + 1)/({m}*2)]"
                            f"*{self.__Dx[x + defer]}/{self.__Dx[x]}")
        return aux

    def t_aax(self, x, m=1, defer=0):
        """
        äxn : Returns the actuarial present value of an (immediate) annuity of 1 per time period
        (whole life annuity-anticipatory), deferred t periods. Payable 'm' per year at the beginning of the period
        :param x: age at the beginning of the contract
        :param m: number of payments per period used to quote the interest rate
        :param defer: deferment period
        :return:Expected Present Value (EPV) for payments of 1/m
        """
        aux = self.aax(x + defer, m) * self.nEx(x, defer)
        if x + defer < self.w:
            self.msn.append(f"{defer}_aax_{x}=[{self.__Nx[x + defer]}/{self.__Dx[x + defer]}-({m}-1)/({m}*2)]"
                            f"*{self.__Dx[x + defer]}/{self.__Dx[x]}")
        return aux

    def t_nax(self, x, n, m=1, defer=0):
        """
        axn : Return the actuarial present value of a (immediate) temporal (term certain) annuity: n-year temporary
        life annuity-late, deferred t periods. Payable 'm' per year at the ends of the period
        :param x: age at the beginning of the contract
        :param n: number of total periods of the interest rate used
        :param m: number of payments per period used to quote the interest rate
        :param defer: deferment period
        :return:Expected Present Value (EPV) for payments of 1/m
        """
        aux = self.nax(x + defer, n, m) * self.nEx(x, defer)
        if x + 1 + n + defer <= self.w:
            self.msn.append(
                f"{defer}|{n}_ax_{x}=[{self.__Nx[x + 1 + defer] - self.__Nx[x + 1 + n + defer]}/{self.__Dx[x + defer]}"
                f"+ ({m}-1)/({m}*2)*(1-{self.__Dx[x + n + defer]}/{self.__Dx[x + defer]})]"
                f"*{self.__Dx[x + defer]}/{self.__Dx[x]}")
        else:
            return self.t_ax(x=x, m=m, defer=defer)
        return aux

    def t_naax(self, x, n, m=1, defer=0):
        """
        näx : Return the actuarial present value of a (immediate) temporal (term certain) annuity: n-year temporary
        life annuity-anticipatory, deferred t periods. Payable 'm' per year at the beginning of the period
        :param x: age at the beginning of the contract
        :param n: number of total periods of the interest rate used
        :param m: number of payments per period used to quote the interest rate
        :param defer: deferment period
        :return: Expected Present Value (EPV) for payments of 1/m
        """
        aux = self.naax(x + defer, n, m) * self.nEx(x, defer)
        if x + 1 + n + defer <= self.w + 1:
            if x + 1 + n + defer <= self.w:
                Nx2 = self.__Nx[x + 1 + n + defer]
            else:
                Nx2 = 0
            self.msn.append(
                f"{defer}|{n}_aax_{x}=[{self.__Nx[x + 1 + defer] - Nx2}/{self.__Dx[x + defer]}"
                f"+({m}+1)/({m}*2)*(1-{self.__Dx[x + n + defer]}/{self.__Dx[x + defer]})]"
                f"*{self.__Dx[x + defer]}/{self.__Dx[x]}")
        else:
            return self.t_aax(x=x, m=m, defer=defer)
        return aux

    '''
    Annuities Increasing and Decreasing Arithmetically
    '''

    # todo: Rita
    def t_nIaax(self, x, n, m=1, defer=0, first_amount=1, increase_amount=1):
        '''

        :param x:
        :param n:
        :param m:
        :param defer:
        :param first_amount:
        :param increase_amount:
        :return:
        '''

        if first_amount + (n - 1) * increase_amount < 0:
            return .0
        if x + n + defer > self.w:
            return .0

        term1 = first_amount * self.t_naax(x=x, n=n, m=m, defer=defer)
        list_increases = [increase_amount * self.t_nax(x=x + defer, n=n - j, m=m, defer=defer + j - 1)
                          for j in range(1, n)]

        return term1 + sum(list_increases)

    def t_nIax(self, x, n, m=1, defer=0, first_amount=1, increase_amount=1):
        '''

        :param x:
        :param n:
        :param m:
        :param defer:
        :param first_amount:
        :param increase_amount:
        :return:
        '''

        if first_amount + (n - 1) * increase_amount < 0:
            return .0
        if x + n + defer > self.w:
            return .0

        term1 = first_amount * self.t_nax(x=x, n=n, m=m, defer=defer)
        list_increases = [increase_amount * self.t_nax(x=x + defer, n=n - j, m=m, defer=defer + j)
                          for j in range(1, n)]

        return term1 + sum(list_increases)

    '''
    Standard types of Variable Life Insurance Increasing and Decreasing Arithmetically
    '''

    # todo: Rita
    def nIAx_g(self, x, n, defer=0, first_amount=1, increase_amount=1):
        '''

        :param x:
        :param n:
        :param increase_amount:
        :param first_amount:
        :return:
        '''

        if first_amount + (n - 1) * increase_amount < 0:
            return .0

        term1 = first_amount * self.t_nAx(x=x, n=n, defer=defer)
        list_increases = [increase_amount * self.t_nAx(x=x + defer, n=n - j, defer=defer + j)
                          for j in range(1, n)]

        return term1 + sum(list_increases)
