"""The real deal."""

from __future__ import annotations

from typing import Callable, Iterable
from .prototype import iscoprime, miller_rabin, multiplicative_integers_mod_n
import itertools
import numpy as np
import seaborn
import polars as pl
import altair as alt

def fp_prime(p: int) -> Callable[[int, int], int]:
    """Function factory for f: (x, y) ==> x / y mod p^3"""
    if p == 3:
        pass
    elif not miller_rabin(p, 15):
        raise Exception(f"P: {p} not prime! (probably)")
    p3 = pow(p, 3)
    def f(x: int, y: int) -> int:
        return moddiv_p3(x, y, p, p3)

    return f

def fp_composite(p: int) -> Callable[[int, int], int]:
    """Function factory for f: (x, y) ==> x / y mod p^3"""
    p3 = pow(p, 3)
    tot = totient(p3)
    def f(x: int, y: int) -> int:
        inv = modular_inverse(tot, y, p3)
        return (x * inv) % p3

    return f

def modular_inverse(totient: int, a: int, n: int) -> int:
    """Return the multiplicative inverse of an integer in Zn*."""
    return pow(a, totient - 1, n)

def tot3(p: int) -> int:
    """Return \phi(p^3) == p^2 * \phi(p), assuming p is prime."""
    return p * p * (p - 1)

def moddiv_p3(x: int, y: int, p: int, p3: int = None) -> int:
    """Compute (x, y) ==> x / y mod p^3."""
    if p3 is None:
        p3 = pow(p, 3)
    # totient = tot3(p)
    totient = tot3(p)
    inv = modular_inverse(totient, y, p3)
    return (x * inv) % p3

def moddiv(x: int, y: int, n: int) -> int:
    """Compute x / y mod n."""
    tot = totient(n)
    inv = modular_inverse(tot, y, n)
    return (x * inv) % n


from sympy.ntheory import factorint

def totient(n: int) -> int:
    """Compute euler's totient function. Credit: https://stackoverflow.com/a/52263174

    Examples
    >>> totient(3)
    2
    >>> totient(9)
    6
    >>> totient(7)
    6
    """
    totient = n
    for factor in factorint(n):
        totient -= totient // factor
    return totient

from enum import Enum
from functools import cached_property

class DivisionClass(Enum):
    PRIME = 1
    COMPOSITE = 2


class NaturalNumber:
    """Wrapper around integers."""

    primes = {3, 5, 7}

    def __init__(self, n: int):
        if n < 0:
            Exception("Natural number must be positive")

        self.n = n

    def __mul__(self, rhs: NaturalNumber):
        if isinstance(rhs, int):
            return NaturalNumber(self.n * rhs)
        elif isinstance(rhs, NaturalNumber):
            return NaturalNumber(self.n * rhs.n)
        else:
            raise ValueError()

    @cached_property
    def division_class(self) -> DivisionClass:
        if miller_rabin(self.n, 20):
            return DivisionClass.PRIME
        else:
            return DivisionClass.COMPOSITE

    def is_prime(self) -> bool:
        if self.n in self.primes: return True
        return self.division_class == DivisionClass.PRIME

    def is_composite(self) -> bool:
        return not self.is_prime()

    def mul_group(self) -> Iterable[int]:
        """Return the multiplicative integers mod n group."""
        if self.is_prime():
            return range(1, self.n)
        else:
            return filter(
                lambda n: iscoprime(n, self.n),
                range(1, self.n)
            )

    def mul_group_list(self) -> list[int]:
        return list(self.mul_group())

    def grid(self) -> np.ndarray:
        if self.is_prime():
            fp = fp_prime(self.n)
        else:
            fp = fp_composite(self.n)

        FP = np.ones((self.n, self.n)) * np.nan

        zn = self.mul_group_list()
        for (i, j) in itertools.product(zn, zn):
            FP[i, j] = fp(j, i)

        return FP

    def inv_grid(self) -> np.ndarray:

        P3 = self.cubed()

        def inv_y(y: int):
            Y = NaturalNumber(y)
            return Y.mul_inv(P3)

        INV = np.ones((1, self.n)) * np.nan

        zn = self.mul_group_list()
        for y in zn:
            INV[0, y] = inv_y(y)

        return INV

    def cubed(self) -> NaturalNumber:
        """Return pow(self, 3)"""
        return NaturalNumber(pow(self.n, 3))

    def inv_df(self) -> pl.DataFrame:
        df = self.df()
        df_s = df.select("p", "p3", "y", "yinv")
        n = len(df_s)
        if self.n % 2 == 0:
            df_half = df_s.slice(0, len(df_s) // 2)
        else:
            print(self.n)
            df_half = df_s.slice(0, self.n - 1)
            # df_half = df_s.slice(0, (n - 1) // 2)
        return df_half.with_columns(y_div_y=pl.col('y') * pl.col('yinv'))

    def df(self) -> pl.DataFrame:
        r"""Return a dataframe with x, y, y^{-1}, (x / y) mod p^3 for all (x, y) \in Zn* \times Zn*"""
        data = self.grid()
        xs: list[int] = []
        ys: list[int] = []
        yinvs: list[int] = []
        x_times_yinvs: list[int] = []
        zs: list[int] = []

        Zn_star = self.mul_group_list()
        P3 = self.cubed()

        for (x, y) in itertools.product(Zn_star, Zn_star):
            xs.append(x)
            ys.append(y)
            zs.append(int(data[y, x]))
            Y = NaturalNumber(y)

            yinv = Y.mul_inv(P3)
            # yinv = modular_inverse(p3 - 1, y, p3)
            yinvs.append(yinv)

            x_times_yinvs.append(x * yinv)


        return pl.DataFrame(dict(
            yinv=yinvs,
            y=ys,
            x=xs,
            x_div_y=x_times_yinvs,
            z=zs,
            p=self.n,
            p3=P3.n,
        ))


    def hist(self):
        return alt.Chart(self.df()).mark_bar().encode(
            x='z',
            y='count()'
        )


    @cached_property
    def totient(self) -> int:
        if self.is_prime():
            return self.n - 1
        else:
            return totient(self.n)

    def mul_inv(self, N: NaturalNumber) -> int:
        """Return the multiplicative inverse of `self`, in the space Z_N*."""
        return modular_inverse(N.totient, self.n, N.n)

    @staticmethod
    def zn(n: int) -> Iterable[int]:
        """Return the multiplicative integers mod n group."""
        N = NaturalNumber(n)
        return N.mul_group()

    @staticmethod
    def fp_grid(p: int) -> np.ndarray:
        """View the graph of fp."""
        N = NaturalNumber(p)
        return N.grid()


    @staticmethod
    def fp_df(p: int) -> pl.DataFrame :
        N = NaturalNumber(p)
        return N.df()

    @staticmethod
    def fp_hist(p: int):
        N = NaturalNumber(p)
        return N.hist()



def fp_grid(p: int):
    return NaturalNumber.fp_grid(p)

def inv_grid(p: int):
    P = NaturalNumber(p)
    return P.inv_grid()


def paint_fp(p: int):
    m = seaborn.heatmap(fp_grid(p))
    m.set_xlabel("x")
    m.set_ylabel("y")

def paint_inf(p: int):
    seaborn.heatmap(inv_grid(p))


def fp_df(p: int):
    return NaturalNumber.fp_df(p)

def fp_hist(p: int):
    return NaturalNumber.fp_hist(p)

def inv_df(p: int):
    P = NaturalNumber(p)
    return P.inv_df()

def simp_df(p: int):
    P = NaturalNumber(p)
    df = P.df()
    return df.select("x", 'y', 'z')